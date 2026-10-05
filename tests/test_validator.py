"""Тесты валидатора."""

import pandas as pd
import pytest

from sap2erp.validator import validate


def test_validate_materials_ok():
    df = pd.DataFrame({
        "Артикул": ["A", "B"],
        "Наименование": ["X", "Y"],
    })
    result = validate(df, "materials")
    assert result.is_valid
    assert result.total_rows == 2


def test_validate_unknown_entity():
    df = pd.DataFrame({"x": [1]})
    with pytest.raises(ValueError, match="Неизвестная сущность"):
        validate(df, "unknown")
