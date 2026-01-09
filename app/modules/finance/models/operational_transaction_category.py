"""Operational transaction category domain model."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class OperationalTransactionCategory:
    """Operational transaction category domain model."""
    
    id: int | None
    name: str
    description: str | None
    icon: str | None
    color: str | None
    is_system: bool
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    text_color: str | None
    bg_color: str | None
    sort_position: int | None
