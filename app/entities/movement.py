"""Movement entity."""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from .base import BaseEntity


class MovementEntity(BaseEntity):
    """Movement between warehouses table."""
    
    __tablename__ = "movements"
    __table_args__ = {'comment': 'Документы перемещения товаров между складами'}
    
    movement_number = Column(String(50), unique=True, nullable=False, index=True, comment="Номер документа перемещения")
    from_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, comment="Склад отправитель")
    to_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, comment="Склад получатель")
    status = Column(String(20), nullable=False, index=True, comment="Статус документа (системный список)")
    planned_date = Column(DateTime, nullable=True, comment="Плановая дата перемещения")
    completed_date = Column(DateTime, nullable=True, comment="Фактическая дата завершения перемещения")

