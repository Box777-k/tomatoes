"""Operational category tree entity."""

from sqlalchemy import Column, Integer, ForeignKey
from .base import BaseEntity


class OperationalCategoryTreeEntity(BaseEntity):
    """Operational category hierarchy table."""
    
    __tablename__ = "operational_category_tree"
    __table_args__ = {'comment': 'Иерархическая структура операционных категорий'}
    
    parent_category_id = Column(Integer, ForeignKey("operational_categories.id"), nullable=True, index=True, comment="Родительская категория")
    child_category_id = Column(Integer, ForeignKey("operational_categories.id"), nullable=False, index=True, comment="Дочерняя категория")
    level = Column(Integer, nullable=False, default=0, comment="Уровень вложенности")
