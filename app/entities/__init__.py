"""Database entities (SQLAlchemy models)."""

from .base import BaseEntity

# Auth entities
from .user import UserEntity
from .role import RoleEntity
from .permission import PermissionEntity
from .user_role import user_roles
from .role_permission import role_permissions

# Business entities
from .order import OrderEntity
from .product import ProductEntity
from .warehouse import WarehouseEntity
from .warehouse_item import WarehouseItemEntity
from .movement import MovementEntity
from .movement_item import MovementItemEntity

# Operational finance entities
from .operational_transaction import OperationalTransactionEntity
from .operational_account import OperationalAccountEntity
from .operational_category import OperationalCategoryEntity
from .operational_category_tree import OperationalCategoryTreeEntity

__all__ = [
    "BaseEntity",
    # Auth
    "UserEntity",
    "RoleEntity",
    "PermissionEntity",
    "user_roles",
    "role_permissions",
    # Business
    "OrderEntity",
    "ProductEntity",
    "WarehouseEntity",
    "WarehouseItemEntity",
    "MovementEntity",
    "MovementItemEntity",
    # Operational finance
    "OperationalTransactionEntity",
    "OperationalAccountEntity",
    "OperationalCategoryEntity",
    "OperationalCategoryTreeEntity",
]

