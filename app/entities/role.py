"""Role entity."""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import BaseEntity


class RoleEntity(BaseEntity):
    """Role table for RBAC."""
    
    __tablename__ = "roles"
    __table_args__ = {'comment': 'Роли пользователей для управления доступом (RBAC)'}
    
    name = Column(String(50), unique=True, nullable=False, index=True, comment="Наименование роли")
    code = Column(String(50), unique=True, nullable=False, index=True, comment="Системный код роли")
    description = Column(String(500), comment="Описание роли и её назначения")
    
    # Relationships
    users = relationship("UserEntity", secondary="user_roles", back_populates="roles")
    permissions = relationship("PermissionEntity", secondary="role_permissions", back_populates="roles")
    
    # Examples: admin, manager, operator, viewer

