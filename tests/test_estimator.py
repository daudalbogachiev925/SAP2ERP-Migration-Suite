"""Тесты оценки бюджета."""

from sap2erp.classifier import ObjectCategory
from sap2erp.estimator import BASE_HOURS, estimate, estimate_one
from sap2erp.inventory import SapObject


def test_estimate_one_base():
    obj = SapObject(name="Z_1", type="PROG", lines=0, used_by=5)
    est = estimate_one(obj, ObjectCategory.CUSTOM_NORMAL, rate=1000)

    assert est.base_hours == BASE_HOURS[ObjectCategory.CUSTOM_NORMAL]
    assert est.adjusted_hours == BASE_HOURS[ObjectCategory.CUSTOM_NORMAL]


def test_estimate_one_with_lines():
    obj = SapObject(name="Z_1", type="PROG", lines=5000, used_by=5)
    est = estimate_one(obj, ObjectCategory.CUSTOM_NORMAL, rate=1000)

    # 30 × (1 + 5000/5000) = 60
    assert est.adjusted_hours == 60


def test_estimate_total():
    objects = [
        SapObject(name="Z_1", type="PROG", lines=0, used_by=5),
        SapObject(name="Z_2", type="PROG", lines=0, used_by=5),
    ]
    categories = {
        "Z_1": ObjectCategory.CUSTOM_NORMAL,
        "Z_2": ObjectCategory.STANDARD_NORMAL,
    }
    budget = estimate(objects, categories, rate=1000)

    assert len(budget.objects) == 2
    assert budget.total_hours == 30 + 5  # base hours
    assert budget.total_cost == (30 + 5) * 1000


def test_by_category():
    objects = [
        SapObject(name="Z_1", type="PROG", lines=0, used_by=5),
        SapObject(name="Z_2", type="PROG", lines=0, used_by=5),
    ]
    categories = {
        "Z_1": ObjectCategory.CUSTOM_NORMAL,
        "Z_2": ObjectCategory.CUSTOM_NORMAL,
    }
    budget = estimate(objects, categories)
    by_cat = budget.by_category()

    assert ObjectCategory.CUSTOM_NORMAL in by_cat
    assert by_cat[ObjectCategory.CUSTOM_NORMAL]["count"] == 2
