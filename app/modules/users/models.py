"""User domain models."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """User domain model."""
    
    id: int | None
    email: str
    first_name: str | None
    last_name: str | None
    phone: str | None
    is_active: bool
    is_superuser: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    
    @property
    def full_name(self) -> str:
        """Get full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or self.email
    
    def activate(self):
        """Activate user."""
        self.is_active = True
    
    def deactivate(self):
        """Deactivate user."""
        self.is_active = False
    
    def verify(self):
        """Verify user email."""
        self.is_verified = True

