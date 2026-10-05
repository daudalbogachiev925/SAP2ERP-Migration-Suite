"""ETL-модули для трансформации SAP-данных в формат 1С:ERP."""

from sap2erp.etl.materials import transform_materials, validate_materials
from sap2erp.etl.customers import transform_customers, validate_customers
from sap2erp.etl.mapping import UNIT_MAP, GROUP_MAP, TYPE_MAP

__all__ = [
    "transform_materials",
    "validate_materials",
    "transform_customers",
    "validate_customers",
    "UNIT_MAP",
    "GROUP_MAP",
    "TYPE_MAP",
]
