"""Product entity."""

from sqlalchemy import Column, String
from .base import BaseEntity


class ProductEntity(BaseEntity):
    """Product table."""
    
    __tablename__ = "products"
    __table_args__ = {'comment': 'Справочник номенклатуры (товары и продукция)'}
    
    name = Column(String(200), nullable=False, comment="Наименование номенклатуры")
    sku = Column(String(50), unique=True, nullable=False, index=True, comment="Артикул (уникальный код товара)")
    description = Column(String(1000), comment="Описание номенклатуры")
    unit = Column(String(20), nullable=False, comment="Единица измерения (системный список)")

