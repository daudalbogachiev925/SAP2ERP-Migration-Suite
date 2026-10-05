# SAP2ERP Migration Suite

Пайплайн миграции мастер-данных SAP → 1С:ERP.

[![CI](https://github.com/USERNAME/sap2erp-migration/actions/workflows/ci.yml/badge.svg)](https://github.com/USERNAME/sap2erp-migration/actions)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Проблема

Холдинги мигрируют с SAP на 1С:ERP по программе импортозамещения (Росатом, Уралхим, Россети). Объём: 5 000–50 000 объектов SAP. Перенос мастер-данных — самый рискованный этап: ошибки на входе ломают учёт на годы.

## Решение

Полный пайплайн миграции:

1. **Инвентаризация** — парсинг выгрузки SAP Solution Manager.
2. **Классификация** — custom/standard, critical/normal.
3. **Оценка** — трудозатраты и бюджет в рублях.
4. **ETL** — трансформация мастер-данных (номенклатура, контрагенты, счета).
5. **Валидация** — обязательные поля, дубликаты, ссылочная целостность.
6. **Экспорт** — CSV/XML для загрузки в 1С:ERP.

## Возможности

- Загрузка инвентаря SAP из Excel/CSV.
- Классификация объектов по 4 категориям.
- Оценка часов и бюджета с параметризацией ставки.
- Маппинг SAP → 1С: ERP-типы, единицы измерения, группы.
- Трансформация материалов, контрагентов, счетов.
- Валидация с отчётом ошибок.
- Экспорт в формат 1С:ERP.
- CLI-интерфейс.

## Установка

```bash
pip install sap2erp-migration
```

Для разработки:

```bash
git clone https://github.com/USERNAME/sap2erp-migration
cd sap2erp-migration
pip install -e ".[dev]"
```

## Использование

### Полный пайплайн

```bash
sap2erp migrate --inventory sap_inventory.xlsx --materials sap_materials.csv --customers sap_customers.csv --output-dir out/
```

### Отдельные команды

```bash
# 1. Инвентаризация
sap2erp inventory --input sap_inventory.xlsx --output report.json

# 2. Классификация
sap2erp classify --input sap_inventory.xlsx --output classified.csv

# 3. Оценка
sap2erp estimate --input classified.csv --rate 3500 --output budget.csv

# 4. ETL
sap2erp etl --materials sap_materials.csv --out 1c_nomenclature.csv
sap2erp etl --customers sap_customers.csv --out 1c_contractors.csv

# 5. Валидация
sap2erp validate --input 1c_nomenclature.csv --rules materials
```

### Пример вывода

```
SAP2ERP Migration Suite
========================
Инвентарь: 5 000 объектов

Классификация:
  custom_critical:    1 250 (25%)
  custom_normal:      2 100 (42%)
  standard_critical:    450 (9%)
  standard_normal:    1 200 (24%)

Оценка трудозатрат:
  Всего часов: 187 500
  Бюджет: 656 250 000 руб

ETL:
  Номенклатура: 10 000 → 9 987 (13 дубликатов удалено)
  Контрагенты:  5 000 → 4 998

Экспорт:
  out/1c_nomenclature.csv
  out/1c_contractors.csv
```

## Архитектура

```
SAP (Solution Manager) ─── inventory.xlsx
        │
        ▼
  ┌──────────────┐
  │  inventory   │  ← парсинг
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  classifier  │  ← custom/standard, critical/normal
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  estimator   │  ← часы + бюджет
  └──────┬───────┘
         ▼
  ┌──────────────────────────────────┐
  │  ETL                             │
  │  materials → 1С Номенклатура     │
  │  customers → 1С Контрагенты      │
  │  gl_accounts → 1С План счетов    │
  └──────┬───────────────────────────┘
         ▼
  ┌──────────────┐
  │  validator   │  ← обязательные поля, дубликаты
  └──────┬───────┘
         ▼
  1С:ERP (CSV/XML)
```

## Структура

```
sap2erp-migration/
├── src/sap2erp/
│   ├── inventory.py
│   ├── classifier.py
│   ├── estimator.py
│   ├── etl/
│   │   ├── materials.py
│   │   ├── customers.py
│   │   └── mapping.py
│   ├── validator.py
│   ├── exporter.py
│   └── cli.py
├── configs/mapping.yaml
├── tests/
└── docs/
```

## Разработка

```bash
make install     # установка
make dev         # dev-зависимости
make test        # тесты
make lint        # ruff + mypy
make format      # black
```

## Лицензия

MIT — см. [LICENSE](LICENSE).

## Контакты

- Автор: Your Name
- Email: you@example.com
