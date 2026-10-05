"""Общие фикстуры для тестов."""

import pandas as pd
import pytest


@pytest.fixture
def sample_sap_materials() -> pd.DataFrame:
    """Образец SAP-номенклатуры."""
    return pd.DataFrame({
        "MATNR": ["MAT00000001", "MAT00000002", "MAT00000003"],
        "MAKTX": ["Материал A", "Материал B", "Материал C"],
        "MEINS": ["ST", "KG", "L"],
        "MATKL": ["RAW", "FIN", "PACK"],
        "MTART": ["ROH", "FERT", "HALB"],
    })


@pytest.fixture
def sample_sap_customers() -> pd.DataFrame:
    """Образец SAP-контрагентов."""
    return pd.DataFrame({
        "KUNNR": ["K00000001", "K00000002"],
        "NAME1": ["ООО Ромашка", "АО Василёк"],
        "STCD1": ["7701234567", "7707654321"],
        "ORT01": ["Москва", "СПб"],
        "LAND1": ["RU", "RU"],
    })
