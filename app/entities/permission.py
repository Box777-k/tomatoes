"""Permission entity."""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import BaseEntity


class PermissionEntity(BaseEntity):
    """Permission table for RBAC."""
    
    __tablename__ = "permissions"
    __table_args__ = {'comment': 'Разрешения на выполнение действий в системе'}
    
    name = Column(String(100), unique=True, nullable=False, index=True, comment="Наименование разрешения")
    code = Column(String(100), unique=True, nullable=False, index=True, comment="Системный код разрешения")
    resource = Column(String(50), nullable=False, index=True, comment="Ресурс системы (системный список)")
    action = Column(String(50), nullable=False, comment="Действие с ресурсом (системный список)")
    description = Column(String(500), comment="Описание разрешения")
    
    # Relationships
    roles = relationship("RoleEntity", secondary="role_permissions", back_populates="permissions")
    
    # Examples:
    # production:orders:create
    # warehouse:items:read
    # finance:transactions:delete

