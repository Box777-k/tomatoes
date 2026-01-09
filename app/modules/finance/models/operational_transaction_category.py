"""Operational transaction category domain model."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class OperationalTransactionCategory:
    """Operational transaction category domain model."""
    
    id: int | None
    name: str
    description: str | None
    parent_id: int | None
    icon: str | None
    text_color: str | None
    bg_color: str | None
    sort_position: int | None
    is_active: bool
    is_system: bool
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    
    def is_system_category(self) -> bool:
        """Check if this is a system category."""
        return self.is_system
    
    def can_be_deleted(self) -> bool:
        """Check if category can be deleted."""
        return not self.is_system and not self.is_deleted
    
    def get_full_path(self) -> str:
        """Get full path in category tree (to be implemented with repository)."""
        # This method will need repository to traverse parent chain
        # For now return just the name
        return self.name
    
    def get_children(self) -> list["OperationalTransactionCategory"]:
        """Get child categories (to be implemented with repository)."""
        # This method will need repository to fetch children
        # For now return empty list
        return []
