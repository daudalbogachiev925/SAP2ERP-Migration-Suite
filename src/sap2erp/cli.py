"""CLI для SAP2ERP Migration Suite."""

from __future__ import annotations

import json
from pathlib import Path

import click
import pandas as pd
from rich.console import Console
from rich.table import Table

from sap2erp.classifier import classify_all
from sap2erp.estimator import estimate
from sap2erp.etl.customers import transform_customers
from sap2erp.etl.materials import transform_materials
from sap2erp.exporter import export_csv
from sap2erp.inventory import InventoryReader
from sap2erp.validator import validate

console = Console()


@click.group()
@click.version_option()
def main() -> None:
    """SAP2ERP Migration Suite — миграция мастер-данных SAP → 1С:ERP."""


@main.command()
@click.option("--input", "-i", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--output", "-o", type=click.Path(path_type=Path), default="inventory.json")
def inventory(input: Path, output: Path) -> None:
    """Парсинг инвентаря SAP."""
    reader = InventoryReader(input)
    objects = reader.read()

    console.print(f"[bold cyan]Инвентарь: {len(objects)} объектов[/bold cyan]")

    # Сводка по типам
    types: dict[str, int] = {}
    for obj in objects:
        types[obj.type] = types.get(obj.type, 0) + 1

    table = Table(title="Объекты по типам")
    table.add_column("Тип")
    table.add_column("Количество", justify="right")
    for t, count in sorted(types.items(), key=lambda x: -x[1]):
        table.add_row(t, str(count))
    console.print(table)

    reader.to_dataframe(objects).to_json(output, orient="records", force_ascii=False, indent=2)
    console.print(f"\n[green]Сохранено: {output}[/green]")


@main.command()
@click.option("--input", "-i", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--output", "-o", type=click.Path(path_type=Path), default="classified.csv")
def classify(input: Path, output: Path) -> None:
    """Классификация объектов SAP."""
    reader = InventoryReader(input)
    objects = reader.read()
    categories = classify_all(objects)

    df = reader.to_dataframe(objects)
    df["category"] = df["object"].map(categories)
    df.to_csv(output, index=False)

    table = Table(title="Классификация")
    table.add_column("Категория")
    table.add_column("Количество", justify="right")
    for cat, count in df["category"].value_counts().items():
        table.add_row(str(cat), str(count))
    console.print(table)
    console.print(f"\n[green]Сохранено: {output}[/green]")


@main.command()
@click.option("--input", "-i", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--rate", "-r", type=float, default=3500, help="Ставка руб/час")
@click.option("--output", "-o", type=click.Path(path_type=Path), default="budget.json")
def estimate_cmd(input: Path, rate: float, output: Path) -> None:
    """Оценка бюджета миграции."""
    reader = InventoryReader(input)
    objects = reader.read()
    categories = classify_all(objects)
    budget = estimate(objects, categories, rate=rate)

    console.print(f"[bold cyan]Оценка бюджета (ставка {rate} руб/час)[/bold cyan]\n")

    table = Table()
    table.add_column("Категория")
    table.add_column("Объектов", justify="right")
    table.add_column("Часов", justify="right")
    table.add_column("Стоимость, руб", justify="right")

    for cat, data in budget.by_category().items():
        table.add_row(
            str(cat.value),
            str(int(data["count"])),
            f"{data['hours']:,.0f}",
            f"{data['cost']:,.0f}",
        )
    console.print(table)

    console.print(f"\n[bold]Всего часов:[/bold] {budget.total_hours:,.0f}")
    console.print(f"[bold]Бюджет:[/bold
