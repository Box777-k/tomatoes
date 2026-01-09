"""Warehouse item entity."""

from sqlalchemy import Column, Integer, ForeignKey, Numeric
from .base import BaseEntity


class WarehouseItemEntity(BaseEntity):
    """Warehouse item (stock) table."""
    
    __tablename__ = "warehouse_items"
    __table_args__ = {'comment': 'Остатки товаров на складах'}
    
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, index=True, comment="Идентификатор склада")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True, comment="Идентификатор номенклатуры")
    quantity = Column(Numeric(10, 2), nullable=False, default=0, comment="Количество в наличии")
    reserved_quantity = Column(Numeric(10, 2), nullable=False, default=0, comment="Зарезервированное количество")

