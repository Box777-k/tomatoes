"""User entity."""

from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.entities.base import BaseEntity


class UserEntity(BaseEntity):
    """User table with FastAPI-Users integration."""
    
    __tablename__ = "users"
    __table_args__ = {'comment': 'Пользователи системы'}
    
    # FastAPI-Users required fields
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False, comment="Email пользователя (для входа в систему)")
    hashed_password: Mapped[str] = mapped_column(String(1024), nullable=False, comment="Хэшированный пароль")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="Активность пользователя (может входить в систему)")
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="Признак суперпользователя (полный доступ)")
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="Подтверждение email пользователя")
    
    # FastAPI-Users required fields (inherited from SQLAlchemyBaseUserTable)
    # id, email, hashed_password, is_active, is_superuser, is_verified
    
    # Additional custom fields
    first_name = Column(String(100), comment="Имя пользователя")
    last_name = Column(String(100), comment="Фамилия пользователя")
    phone = Column(String(20), comment="Телефон пользователя")
    
    
    # Relationships
    roles = relationship("RoleEntity", secondary="user_roles", back_populates="users")

