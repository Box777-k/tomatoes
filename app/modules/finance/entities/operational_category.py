"""Operational finance category entity."""

from sqlalchemy import Column, String, Boolean, Integer
from app.entities.base import BaseEntity


class OperationalCategoryEntity(BaseEntity):
    """Operational finance transaction category table."""
    
    __tablename__ = "operational_categories"
    __table_args__ = {'comment': 'Операционный справочник категорий финансовых транзакций'}
    
    # Main
    name = Column(String(200), nullable=False, comment="Наименование категории")
    description = Column(String, nullable=True, comment="Описание категории")
    
    # UI
    icon = Column(String(50), nullable=True, comment="Иконка для UI")
    text_color = Column(String(7), nullable=True, comment="Цвет текста для визуального отображения (HEX)")
    bg_color = Column(String(7), nullable=True, comment="Цвет фона для визуального отображения (HEX)")
    
    # Data sort
    sort_position = Column(Integer, nullable=True, default=0, comment="Позиция сортировки")
    
    # System
    is_active = Column(Boolean, nullable=False, default=True, comment="Признак активности категории")
    is_system = Column(Boolean, nullable=False, default=False, comment="Системная категория (не удаляемая)")
