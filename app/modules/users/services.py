"""User services."""

from datetime import datetime

from .repositories import UserRepository
from .models import User
from app.core.exceptions import ValidationException, EntityNotFoundException
from app.core.security import get_password_hash


class UserService:
    """Service for user business logic."""
    
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    async def get_all_users(self) -> list[User]:
        """Get all users."""
        return await self.repo.find_all()
    
    async def get_user(self, user_id: int) -> User:
        """Get user by ID."""
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id)
        return user
    
    async def create_user(
        self,
        email: str,
        password: str,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        is_superuser: bool = False
    ) -> User:
        """Create new user."""
        # Validate email uniqueness
        existing = await self.repo.get_by_email(email)
        if existing:
            raise ValidationException(f"User with email {email} already exists")
        
        # Hash password
        hashed_password = get_password_hash(password)
        
        # Create user
        user = User(
            id=None,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            is_active=True,
            is_superuser=is_superuser,
            is_verified=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_deleted=False
        )
        
        # Save with hashed password
        return await self.repo.create_with_password(user, hashed_password)
    
    async def update_user(
        self,
        user_id: int,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None
    ) -> User:
        """Update user."""
        user = await self.get_user(user_id)
        
        if email and email != user.email:
            existing = await self.repo.get_by_email(email)
            if existing and existing.id != user_id:
                raise ValidationException(f"Email {email} already in use")
            user.email = email
        
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if phone is not None:
            user.phone = phone
        
        user.updated_at = datetime.now()
        return await self.repo.save(user)
    
    async def activate_user(self, user_id: int) -> User:
        """Activate user."""
        user = await self.get_user(user_id)
        user.activate()
        return await self.repo.save(user)
    
    async def deactivate_user(self, user_id: int) -> User:
        """Deactivate user."""
        user = await self.get_user(user_id)
        user.deactivate()
        return await self.repo.save(user)
    
    async def delete_user(self, user_id: int):
        """Delete user (soft delete)."""
        await self.repo.delete(user_id)

