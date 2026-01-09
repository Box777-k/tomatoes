"""Base entity class for all database tables."""

from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, DateTime, String
from sqlalchemy.sql import func
from app.core.database import Base


class BaseEntity(Base):
    """Base entity with common fields."""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True, comment="Уникальный идентификатор записи")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="Дата и время создания записи")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="Дата и время последнего изменения записи")
    is_deleted = Column(Boolean, server_default="false", nullable=False, comment="Признак удаления записи (мягкое удаление)")

    text_color = Column(String(20), nullable=True, comment="Цвет текста для UI (hex код)")
    bg_color = Column(String(20), nullable=True, comment="Цвет фона для UI (hex код)")
    sort_position = Column(Integer, nullable=True, comment="Позиция при сортировке")
     