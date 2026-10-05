"""ETL для контрагентов SAP → 1С."""

from __future__ import annotations

import pandas as pd

from sap2erp.etl.mapping import COUNTRY_MAP

REQUIRED_COLUMNS = {"KUNNR", "NAME1"}


def transform_customers(sap_df: pd.DataFrame) -> pd.DataFrame:
    """Трансформирует контрагентов SAP → формат 1С."""
    missing = REQUIRED_COLUMNS - set(sap_df.columns)
    if missing:
        raise ValueError(f"Отсутствуют колонки SAP: {missing}")

    result = pd.DataFrame()

    result["Наименование"] = sap_df["NAME1"].astype(str).str.strip()
    result["SAP_ID"] = sap_df["KUNNR"].astype(str)

    # ИНН (если есть)
    if "STCD1" in sap_df.columns:
        result["ИНН"] = sap_df["STCD1"].astype(str).str.strip()
    else:
        result["ИНН"] = ""

    # Город
    if "ORT01" in sap_df.columns:
        result["Город"] = sap_df["ORT01"].astype(str).str.strip()
    else:
        result["Город"] = ""

    # Страна
    if "LAND1" in sap_df.columns:
        result["Страна"] = (
            sap_df["LAND1"].astype(str).map(COUNTRY_MAP).fillna(sap_df["LAND1"])
        )
    else:
        result["Страна"] = "Россия"

    return result


def validate_customers(df: pd.DataFrame) -> list[str]:
    """Валидирует контрагентов."""
    errors: list[str] = []

    if df["Наименование"].isna().any():
        errors.append(f"Пустых наименований: {df['Наименование'].isna().sum()}")

    # ИНН: 10 или 12 цифр (если заполнен)
    def is_valid_inn(inn: str) -> bool:
        if not inn or inn == "nan":
            return True
        digits = "".join(c for c in inn if c.isdigit())
        return len(digits) in (10, 12)

    invalid_inn = df["ИНН"].apply(lambda x: not is_valid_inn(str(x))).sum()
    if invalid_inn > 0:
        errors.append(f"Некорректных ИНН: {invalid_inn}")

    return errors
