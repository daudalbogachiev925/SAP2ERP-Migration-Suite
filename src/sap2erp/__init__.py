"""SAP2ERP Migration Suite — миграция мастер-данных SAP → 1С:ERP."""

__version__ = "0.1.0"

from sap2erp.inventory import InventoryReader, SapObject
from sap2erp.classifier import classify, ObjectCategory
from sap2erp.estimator import estimate, BudgetEstimate

__all__ = [
    "__version__",
    "InventoryReader",
    "SapObject",
    "classify",
    "ObjectCategory",
    "estimate",
    "BudgetEstimate",
]
