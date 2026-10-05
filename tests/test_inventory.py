"""Тесты загрузки инвентаря."""

from pathlib import Path

import pandas as pd
import pytest

from sap2erp.inventory import InventoryReader, SapObject


def test_read_csv(tmp_path: Path):
    csv = tmp_path / "inv.csv"
    pd.DataFrame({
        "object": ["Z_PROG_1", "SAP_STD_1"],
        "type": ["PROG", "FUNC"],
        "lines": [500, 100],
        "used_by": [10, 5],
    }).to_csv(csv, index=False)

    reader = InventoryReader(csv)
    objects = reader.read()

    assert len(objects) == 2
    assert objects[0].name == "Z_PROG_1"
    assert objects[0].type == "PROG"
    assert objects[0].lines == 500


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        InventoryReader(Path("/tmp/nonexistent_file.csv"))


def test_missing_columns(tmp_path: Path):
    csv = tmp_path / "bad.csv"
    pd.DataFrame({"object": ["X"]}).to_csv(csv, index=False)

    reader = InventoryReader(csv)
    with pytest.raises(ValueError, match="Отсутствуют обязательные колонки"):
        reader.read()


def test_to_dataframe():
    objects = [
        SapObject(name="Z_1", type="PROG", lines=100, used_by=5),
        SapObject(name="Z_2", type="FUNC", lines=200, used_by=10),
    ]
    df = InventoryReader.to_dataframe(objects)

    assert len(df) == 2
    assert list(df.columns) == ["object", "type", "lines", "used_by", "last_modified"]
