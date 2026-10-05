"""Классификация объектов SAP по категориям."""

from __future__ import annotations

from enum import Enum

from sap2erp.inventory import SapObject


class ObjectCategory(str, Enum):
    """Категория объекта SAP."""

    CUSTOM_CRITICAL = "custom_critical"
    CUSTOM_NORMAL = "custom_normal"
    STANDARD_CRITICAL = "standard_critical"
    STANDARD_NORMAL = "standard_normal"


# Пороги для critical
CRITICAL_USED_BY = 50
CRITICAL_LINES = 3000

# Префиксы кастомных объектов SAP
CUSTOM_PREFIXES = ("Z_", "Y_")


def _is_custom(obj: SapObject) -> bool:
    """Z_* и Y_* — кастомные объекты SAP."""
    return obj.name.startswith(CUSTOM_PREFIXES)


def _is_critical(obj: SapObject) -> bool:
    """Critical: много строк кода или много пользователей."""
    return obj.used_by >= CRITICAL_USED_BY or obj.lines >= CRITICAL_LINES


def classify(obj: SapObject) -> ObjectCategory:
    """Классифицирует объект SAP.

    Args:
        obj: объект SAP.

    Returns:
        ObjectCategory.
    """
    custom = _is_custom(obj)
    critical = _is_critical(obj)

    if custom and critical:
        return ObjectCategory.CUSTOM_CRITICAL
    if custom:
        return ObjectCategory.CUSTOM_NORMAL
    if critical:
        return ObjectCategory.STANDARD_CRITICAL
    return ObjectCategory.STANDARD_NORMAL


def classify_all(objects: list[SapObject]) -> dict[str, ObjectCategory]:
    """Классифицирует список объектов.

    Returns:
        Словарь {имя_объекта: категория}.
    """
    return {obj.name: classify(obj) for obj in objects}
