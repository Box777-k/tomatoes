"""User entity-domain mappers."""

from app.entities import UserEntity
from .models import User


class UserMapper:
    """Mapper for User entity <-> domain model."""
    
    @staticmethod
    def to_domain(entity: UserEntity) -> User:
        """Convert entity to domain model."""
        return User(
            id=entity.id,
            email=entity.email,
            first_name=entity.first_name,
            last_name=entity.last_name,
            phone=entity.phone,
            is_active=entity.is_active,
            is_superuser=entity.is_superuser,
            is_verified=entity.is_verified,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_deleted=entity.is_deleted,
        )
    
    @staticmethod
    def to_entity(model: User) -> UserEntity:
        """Convert domain model to entity."""
        entity = UserEntity()
        entity.id = model.id
        entity.email = model.email
        entity.first_name = model.first_name
        entity.last_name = model.last_name
        entity.phone = model.phone
        entity.is_active = model.is_active
        entity.is_superuser = model.is_superuser
        entity.is_verified = model.is_verified
        entity.created_at = model.created_at
        entity.updated_at = model.updated_at
        entity.is_deleted = model.is_deleted
        return entity

