"""Загрузка инвентаря объектов SAP."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class SapObject:
    """Один объект SAP из инвентаря."""

    name: str
    type: str
    lines: int
    used_by: int
    last_modified: str = ""


class InventoryReader:
    """Читает инвентарь SAP из Excel или CSV."""

    # Обязательные колонки в файле
    REQUIRED_COLUMNS = {"object", "type", "lines", "used_by"}

    def __init__(self, path: Path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"Файл не найден: {self.path}")

    def read(self) -> list[SapObject]:
        """Читает и валидирует инвентарь."""
        if self.path.suffix in (".xlsx", ".xls"):
            df = pd.read_excel(self.path)
        elif self.path.suffix == ".csv":
            df = pd.read_csv(self.path)
        else:
            raise ValueError(f"Неподдерживаемый формат: {self.path.suffix}")

        missing = self.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"Отсутствуют обязательные колонки: {missing}")

        objects = []
        for _, row in df.iterrows():
            objects.append(
                SapObject(
                    name=str(row["object"]),
                    type=str(row["type"]),
                    lines=int(row["lines"]),
                    used_by=int(row["used_by"]),
                    last_modified=str(row.get("last_modified", "")),
                )
            )
        return objects

    @staticmethod
    def to_dataframe(objects: list[SapObject]) -> pd.DataFrame:
        """Конвертирует объекты в DataFrame."""
        return pd.DataFrame(
            [
                {
                    "object": o.name,
                    "type": o.type,
                    "lines": o.lines,
                    "used_by": o.used_by,
                    "last_modified": o.last_modified,
                }
                for o in objects
            ]
        )
