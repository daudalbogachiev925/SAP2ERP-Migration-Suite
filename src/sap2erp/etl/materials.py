"""ETL для номенклатуры SAP → 1С."""

from __future__ import annotations

import pandas as pd

from sap2erp.etl.mapping import GROUP_MAP, TYPE_MAP, UNIT_MAP

# Ожидаемые колонки SAP
REQUIRED_COLUMNS = {"MATNR", "MAKTX", "MEINS"}


def transform_materials(sap_df: pd.DataFrame) -> pd.DataFrame:
    """Трансформирует номенклатуру SAP → формат 1С.

    Args:
        sap_df: DataFrame с колонками MATNR, MAKTX, MEINS, MATKL, MTART.

    Returns:
        DataFrame для загрузки в 1С:ERP.

    Raises:
        ValueError: если не хватает обязательных колонок.
    """
    missing = REQUIRED_COLUMNS - set(sap_df.columns)
    if missing:
        raise ValueError(f"Отсутствуют колонки SAP: {missing}")

    result = pd.DataFrame()

    # Артикул (SAP MATNR → 1С Артикул)
    result["Артикул"] = sap_df["MATNR"].astype(str).str.strip()

    # Наименование (MAKTX → Наименование)
    result["Наименование"] = sap_df["MAKTX"].astype(str).str.strip()

    # Единица измерения
    if "MEINS" in sap_df.columns:
        result["ЕдиницаИзмерения"] = (
            sap_df["MEINS"].astype(str).map(UNIT_MAP).fillna(sap_df["MEINS"])
        )
    else:
        result["ЕдиницаИзмерения"] = "шт"

    # Группа
    if "MATKL" in sap_df.columns:
        result["Группа"] = (
            sap_df["MATKL"].astype(str).map(GROUP_MAP).fillna(sap_df["MATKL"])
        )
    else:
        result["Группа"] = "Прочее"

    # Вид номенклатуры
    if "MTART" in sap_df.columns:
        result["ВидНоменклатуры"] = (
            sap_df["MTART"].astype(str).map(TYPE_MAP).fillna("Материал")
        )
    else:
        result["ВидНоменклатуры"] = "Материал"

    # Сохраняем SAP_ID для трассировки
    result["SAP_ID"] = sap_df["MATNR"].astype(str)

    return result


def validate_materials(df: pd.DataFrame) -> list[str]:
    """Валидирует трансформированный DataFrame.

    Returns:
        Список сообщений об ошибках (пустой, если всё ок).
    """
    errors: list[str] = []

    if df["Артикул"].isna().any():
        errors.append(f"Пустых артикулов: {df['Артикул'].isna().sum()}")

    if df["Артикул"].duplicated().any():
        dups = df["Артикул"][df["Артикул"].duplicated()].unique()[:5]
        errors.append(f"Дубликаты артикулов (первые 5): {list(dups)}")

    empty_names = (df["Наименование"].astype(str).str.strip() == "").sum()
    if empty_names > 0:
        errors.append(f"Пустых наименований: {empty_names}")

    return errors
