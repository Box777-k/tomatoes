"""User Pydantic schemas."""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for creating user."""
    email: EmailStr
    password: str = Field(min_length=6)
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    is_superuser: bool = False


class UserUpdate(BaseModel):
    """Schema for updating user."""
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    email: str
    first_name: str | None
    last_name: str | None
    phone: str | None
    is_active: bool
    is_superuser: bool
    is_verified: bool
    created_at: datetime
    
    @classmethod
    def from_domain(cls, user):
        """Create from domain model."""
        return cls(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            is_verified=user.is_verified,
            created_at=user.created_at
        )

