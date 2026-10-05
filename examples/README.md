# Примеры данных

В этой папке — примеры выгрузок SAP для тестирования пайплайна.

## Файлы

| Файл | Описание |
|------|----------|
| `sap_inventory_sample.csv` | Инвентарь объектов SAP (программы, функции, классы, таблицы) |
| `sap_materials_sample.csv` | Номенклатура из SAP (MARA) |
| `sap_customers_sample.csv` | Контрагенты из SAP (KNA1) |

## Как использовать

```bash
# 1. Классификация инвентаря
sap2erp classify --input examples/sap_inventory_sample.csv --output classified.csv

# 2. Оценка бюджета
sap2erp estimate --input examples/sap_inventory_sample.csv --rate 3500

# 3. ETL номенклатуры и контрагентов
sap2erp etl \
  --materials examples/sap_materials_sample.csv \
  --customers examples/sap_customers_sample.csv \
  --out out/
```

## Ожидаемые результаты

- 15 объектов в инвентаре, 4 категории.
- 10 позиций номенклатуры, все валидные.
- 5 контрагентов, все с корректными ИНН.
