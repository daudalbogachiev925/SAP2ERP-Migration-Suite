"""Экспорт данных в форматы для загрузки в 1С:ERP."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def export_csv(df: pd.DataFrame, output_path: Path, encoding: str = "utf-8-sig") -> None:
    """Экспорт в CSV (utf-8-sig для корректного открытия в Excel)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding=encoding)


def export_excel(df: pd.DataFrame, output_path: Path) -> None:
    """Экспорт в Excel."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_path, index=False)


def export_json(df: pd.DataFrame, output_path: Path) -> None:
    """Экспорт в JSON (для API-загрузки)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_json(output_path, orient="records", force_ascii=False, indent=2)
