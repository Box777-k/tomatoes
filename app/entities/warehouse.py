"""Warehouse entity."""

from sqlalchemy import Column, String, Boolean
from .base import BaseEntity


class WarehouseEntity(BaseEntity):
    """Warehouse table."""
    
    __tablename__ = "warehouses"
    __table_args__ = {'comment': 'Справочник складов организации'}
    
    name = Column(String(200), nullable=False, comment="Наименование склада")
    code = Column(String(50), unique=True, nullable=False, index=True, comment="Код склада")
    address = Column(String(500), comment="Адрес местонахождения склада")
    is_active = Column(Boolean, default=True, nullable=False, comment="Признак активности склада")

