"""User-Role association entity."""

from sqlalchemy import Column, Integer, ForeignKey, Table
from app.core.database import Base

# Many-to-Many relationship between users and roles
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, comment="Идентификатор пользователя"),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True, comment="Идентификатор роли"),
    comment="Связь пользователей с ролями (многие ко многим)"
)

