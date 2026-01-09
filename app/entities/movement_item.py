"""Movement item entity."""

from sqlalchemy import Column, Integer, ForeignKey, Numeric
from .base import BaseEntity


class MovementItemEntity(BaseEntity):
    """Movement item table."""
    
    __tablename__ = "movement_items"
    __table_args__ = {'comment': 'Позиции документа перемещения (табличная часть)'}
    
    movement_id = Column(Integer, ForeignKey("movements.id"), nullable=False, index=True, comment="Идентификатор документа перемещения")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="Идентификатор номенклатуры")
    quantity = Column(Numeric(10, 2), nullable=False, comment="Количество к перемещению")

