"""Тесты классификатора."""

from sap2erp.classifier import ObjectCategory, classify, classify_all
from sap2erp.inventory import SapObject


def test_custom_critical():
    obj = SapObject(name="Z_BIG_PROG", type="PROG", lines=5000, used_by=100)
    assert classify(obj) == ObjectCategory.CUSTOM_CRITICAL


def test_custom_normal():
    obj = SapObject(name="Z_SMALL", type="PROG", lines=100, used_by=5)
    assert classify(obj) == ObjectCategory.CUSTOM_NORMAL


def test_standard_critical():
    obj = SapObject(name="SAP_STD_BIG", type="FUNC", lines=4000, used_by=80)
    assert classify(obj) == ObjectCategory.STANDARD_CRITICAL


def test_standard_normal():
    obj = SapObject(name="SAP_STD_SMALL", type="TABLE", lines=50, used_by=3)
    assert classify(obj) == ObjectCategory.STANDARD_NORMAL


def test_classify_all():
    objects = [
        SapObject(name="Z_1", type="PROG", lines=100, used_by=5),
        SapObject(name="Z_2", type="PROG", lines=5000, used_by=100),
    ]
    categories = classify_all(objects)

    assert categories["Z_1"] == ObjectCategory.CUSTOM_NORMAL
    assert categories["Z_2"] == ObjectCategory.CUSTOM_CRITICAL
