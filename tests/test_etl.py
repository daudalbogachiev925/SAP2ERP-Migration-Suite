"""Тесты ETL."""

import pandas as pd
import pytest

from sap2erp.etl.customers import transform_customers, validate_customers
from sap2erp.etl.materials import transform_materials, validate_materials


def test_transform_materials(sample_sap_materials):
    result = transform_materials(sample_sap_materials)

    assert len(result) == 3
    assert "Артикул" in result.columns
    assert "Наименование" in result.columns
    assert result.iloc[0]["Артикул"] == "MAT00000001"
    assert result.iloc[0]["ЕдиницаИзмерения"] == "шт"  # ST
    assert result.iloc[1]["ЕдиницаИзмерения"] == "кг"  # KG
    assert result.iloc[0]["Группа"] == "Сырьё"  # RAW
    assert result.iloc[1]["Группа"] == "Готовая продукция"  # FIN


def test_transform_materials_missing_columns():
    df = pd.DataFrame({"foo": [1]})
    with pytest.raises(ValueError, match="Отсутствуют колонки SAP"):
        transform_materials(df)


def test_validate_materials_ok(sample_sap_materials):
    result = transform_materials(sample_sap_materials)
    errors = validate_materials(result)
    assert errors == []


def test_validate_materials_duplicates():
    df = pd.DataFrame({
        "Артикул": ["A", "A", "B"],
        "Наименование": ["X", "Y", "Z"],
    })
    errors = validate_materials(df)
    assert any("Дубликаты" in e for e in errors)


def test_transform_customers(sample_sap_customers):
    result = transform_customers(sample_sap_customers)

    assert len(result) == 2
    assert result.iloc[0]["Наименование"] == "ООО Ромашка"
    assert result.iloc[0]["ИНН"] == "7701234567"
    assert result.iloc[0]["Город"] == "Москва"
    assert result.iloc[0]["Страна"] == "Россия"


def test_validate_customers_invalid_inn():
    df = pd.DataFrame({
        "Наименование": ["X"],
        "ИНН": ["123"],  # слишком короткий
    })
    errors = validate_customers(df)
    assert any("Некорректных ИНН" in e for e in errors)
