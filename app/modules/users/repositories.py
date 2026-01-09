"""User repositories."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.future import select

from app.entities import UserEntity
from .models import User
from .mappers import UserMapper


class UserRepository:
    """Repository for User entity."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.mapper = UserMapper()
    
    async def get_by_id(self, user_id: int) -> User | None:
        """Get user by ID."""
        result = await self.session.execute(
            select(UserEntity).where(
                UserEntity.id == user_id,
                UserEntity.is_deleted == False
            )
        )
        entity = result.scalar_one_or_none()
        return self.mapper.to_domain(entity) if entity else None
    
    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        result = await self.session.execute(
            select(UserEntity).where(
                UserEntity.email == email,
                UserEntity.is_deleted == False
            )
        )
        entity = result.scalar_one_or_none()
        return self.mapper.to_domain(entity) if entity else None
    
    async def find_all(self) -> list[User]:
        """Get all users."""
        result = await self.session.execute(
            select(UserEntity).where(UserEntity.is_deleted == False)
        )
        entities = result.scalars().all()
        return [self.mapper.to_domain(e) for e in entities]
    
    async def create_with_password(self, user: User, hashed_password: str) -> User:
        """Create new user with password."""
        entity = self.mapper.to_entity(user)
        entity.hashed_password = hashed_password
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return self.mapper.to_domain(entity)
    
    async def save(self, user: User) -> User:
        """Save user."""
        if user.id:
            # Update existing
            entity = await self.session.get(UserEntity, user.id)
            if entity:
                entity.email = user.email
                entity.first_name = user.first_name
                entity.last_name = user.last_name
                entity.phone = user.phone
                entity.is_active = user.is_active
                entity.is_superuser = user.is_superuser
                entity.is_verified = user.is_verified
        else:
            # Create new
            entity = self.mapper.to_entity(user)
            self.session.add(entity)
        
        await self.session.flush()
        await self.session.refresh(entity)
        return self.mapper.to_domain(entity)
    
    async def delete(self, user_id: int):
        """Soft delete user."""
        entity = await self.session.get(UserEntity, user_id)
        if entity:
            entity.is_deleted = True
            await self.session.flush()

