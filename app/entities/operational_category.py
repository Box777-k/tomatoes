"""Operational category entity."""

from sqlalchemy import Column, String, Boolean
from .base import BaseEntity


class OperationalCategoryEntity(BaseEntity):
    """Operational transaction category table."""
    
    __tablename__ = "operational_categories"
    __table_args__ = {'comment': 'Справочник категорий операционных финансовых операций'}
    
    name = Column(String(200), nullable=False, comment="Наименование категории")
    description = Column(String, nullable=True, comment="Описание категории")
    icon = Column(String(50), nullable=True, comment="Иконка для UI")
    color = Column(String(20), nullable=True, comment="Цвет для UI (hex код)")
    is_system = Column(Boolean, nullable=False, default=False, comment="Системная категория (не удаляемая)")
