"""Общий валидатор ETL-результатов."""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from sap2erp.etl.customers import validate_customers
from sap2erp.etl.materials import validate_materials


@dataclass
class ValidationResult:
    """Результат валидации."""

    entity: str
    total_rows: int
    errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


# Реестр валидаторов по имени сущности
VALIDATORS = {
    "materials": validate_materials,
    "customers": validate_customers,
}


def validate(df: pd.DataFrame, entity: str) -> ValidationResult:
    """Валидирует DataFrame по имени сущности.

    Args:
        df: DataFrame для валидации.
        entity: "materials" | "customers".

    Returns:
        ValidationResult.

    Raises:
        ValueError: если сущность не поддерживается.
    """
    if entity not in VALIDATORS:
        raise ValueError(
            f"Неизвестная сущность: {entity}. "
            f"Доступные: {list(VALIDATORS.keys())}"
        )

    errors = VALIDATORS[entity](df)
    return ValidationResult(
        entity=entity,
        total_rows=len(df),
        errors=errors,
    )
