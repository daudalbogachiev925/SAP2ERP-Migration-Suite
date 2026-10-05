"""Оценка трудозатрат и бюджета миграции."""

from __future__ import annotations

from dataclasses import dataclass, field

from sap2erp.classifier import ObjectCategory
from sap2erp.inventory import SapObject


# Базовые часы на объект по категории
BASE_HOURS: dict[ObjectCategory, int] = {
    ObjectCategory.CUSTOM_CRITICAL: 80,
    ObjectCategory.CUSTOM_NORMAL: 30,
    ObjectCategory.STANDARD_CRITICAL: 20,
    ObjectCategory.STANDARD_NORMAL: 5,
}

# Ставка по умолчанию, руб/час
DEFAULT_RATE = 3500


@dataclass
class ObjectEstimate:
    """Оценка одного объекта."""

    name: str
    category: ObjectCategory
    lines: int
    base_hours: int
    adjusted_hours: float
    cost: float


@dataclass
class BudgetEstimate:
    """Итоговая оценка по всем объектам."""

    objects: list[ObjectEstimate] = field(default_factory=list)
    rate: float = DEFAULT_RATE

    @property
    def total_hours(self) -> float:
        return sum(o.adjusted_hours for o in self.objects)

    @property
    def total_cost(self) -> float:
        return sum(o.cost for o in self.objects)

    def by_category(self) -> dict[ObjectCategory, dict[str, float]]:
        """Группировка по категориям."""
        result: dict[ObjectCategory, dict[str, float]] = {}
        for obj in self.objects:
            cat = obj.category
            if cat not in result:
                result[cat] = {"count": 0, "hours": 0.0, "cost": 0.0}
            result[cat]["count"] += 1
            result[cat]["hours"] += obj.adjusted_hours
            result[cat]["cost"] += obj.cost
        return result


def estimate_one(
    obj: SapObject,
    category: ObjectCategory,
    rate: float = DEFAULT_RATE,
) -> ObjectEstimate:
    """Оценивает один объект.

    Формула: базовые часы × (1 + lines / 5000).
    """
    base = BASE_HOURS[category]
    adjusted = base * (1 + obj.lines / 5000)
    cost = adjusted * rate

    return ObjectEstimate(
        name=obj.name,
        category=category,
        lines=obj.lines,
        base_hours=base,
        adjusted_hours=adjusted,
        cost=cost,
    )


def estimate(
    objects: list[SapObject],
    categories: dict[str, ObjectCategory],
    rate: float = DEFAULT_RATE,
) -> BudgetEstimate:
    """Оценивает список объектов."""
    result = BudgetEstimate(rate=rate)
    for obj in objects:
        cat = categories[obj.name]
        result.objects.append(estimate_one(obj, cat, rate))
    return result
