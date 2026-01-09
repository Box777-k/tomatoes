"""Operational transaction category tree domain model."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class OperationalTransactionCategoryTree:
    """Operational transaction category tree domain model."""
    
    id: int | None
    parent_category_id: int | None
    child_category_id: int
    level: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    text_color: str | None
    bg_color: str | None
    sort_position: int | None
