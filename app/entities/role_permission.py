"""Role-Permission association entity."""

from sqlalchemy import Column, Integer, ForeignKey, Table
from app.core.database import Base

# Many-to-Many relationship between roles and permissions
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True, comment="Идентификатор роли"),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True, comment="Идентификатор разрешения"),
    comment="Связь ролей с разрешениями (многие ко многим)"
)

