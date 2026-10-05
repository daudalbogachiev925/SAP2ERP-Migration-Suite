# Архитектура SAP2ERP Migration Suite

## Общая схема

```
┌─────────────────────────────────────────────────────────────┐
│                    SAP Solution Manager                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Inventory  │  │  Materials  │  │  Customers  │        │
│  │  (object    │  │  (MARA)     │  │  (KNA1)     │        │
│  │   list)     │  │             │  │             │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
└─────────┼────────────────┼────────────────┼───────────────┘
          │                │                │
          ▼                │                │
    ┌──────────┐           │                │
    │ inventory│           │                │
    └────┬─────┘           │                │
         ▼                 │                │
    ┌──────────┐           │                │
    │classifier│           │                │
    └────┬─────┘           │                │
         ▼                 │                │
    ┌──────────┐           │                │
    │estimator │           │                │
    └────┬─────┘           │                │
         │                 │                │
         ▼                 ▼                ▼
    budget.json       ┌─────────────────────────┐
                      │         ETL             │
                      │ ┌─────────────────────┐ │
                      │ │ transform_materials │ │
                      │ ├─────────────────────┤ │
                      │ │ transform_customers │ │
                      │ └─────────────────────┘ │
                      └────────────┬────────────┘
                                   │
                                   ▼
                            ┌──────────┐
                            │validator │
                            └────┬─────┘
                                 │
                                 ▼
                          ┌──────────┐
                          │ exporter │
                          └────┬─────┘
                               │
                               ▼
                        1C:ERP (CSV)
```

## Модули

### `inventory.py`
Читает инвентарь объектов SAP из Excel/CSV. Валидирует обязательные колонки. Возвращает список `SapObject`.

### `classifier.py`
Классифицирует объекты SAP по 4 категориям:
- `custom_critical` — кастомный (Z_*), критичный (used_by ≥ 50 или lines ≥ 3000).
- `custom_normal` — кастомный, но небольшой.
- `standard_critical` — стандартный SAP, критичный.
- `standard_normal` — стандартный, незначительный.

### `estimator.py`
Считает трудозатраты по формуле `base_hours × (1 + lines / 5000)`.
Итог: общее количество часов + бюджет в рублях.

### `etl/materials.py`
Трансформация SAP MARA → 1С Номенклатура.
Маппинги: `MEINS → ЕдиницаИзмерения`, `MATKL → Группа`, `MTART → ВидНоменклатуры`.

### `etl/customers.py`
Трансформация SAP KNA1 → 1С Контрагенты.
Маппинг стран: ISO-2 → название.

### `validator.py`
Общий валидатор: обязательные поля, дубликаты, форматы (ИНН 10/12 цифр).

### `exporter.py`
Экспорт в CSV (utf-8-sig для Excel), Excel, JSON.

### `cli.py`
CLI на Click с командами: `inventory`, `classify`, `estimate`, `etl`, `validate`.

## Потоки данных

### Инвентарь и бюджет
```
inventory.csv → InventoryReader → SapObject[]
                                       ↓
                                   classify_all
                                       ↓
                                   estimate
                                       ↓
                                   budget.json
```

### ETL мастер-данных
```
sap_materials.csv → transform_materials → DataFrame → validate → export_csv
sap_customers.csv → transform_customers → DataFrame → validate → export_csv
```

## Расширение

### Добавить новую сущность (например, счета)

1. Создать `src/sap2erp/etl/gl_accounts.py`.
2. Добавить маппинги в `mapping.py`.
3. Зарегистрировать валидатор в `validator.py:VALIDATORS`.
4. Добавить команду в CLI.
5. Написать тесты.

### Добавить экспорт в XML для 1С

Расширить `exporter.py` функцией `export_xml(df, template_path, output_path)`.

### Поддержать другие ERP-источники

Инвентарь можно читать не только из SAP: добавить `OracleReader`, `1CReader` с тем же интерфейсом.
