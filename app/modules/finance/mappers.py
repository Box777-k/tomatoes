"""Finance entity-domain mappers."""

from datetime import datetime
from app.entities import (
    OperationalTransactionEntity, 
    OperationalAccountEntity, 
    OperationalCategoryEntity
)
from .models import (
    OperationalFinanceAccount, 
    OperationalFinanceTransaction, 
    OperationalTransactionCategory
)


class OperationalFinanceAccountMapper:
    """Mapper for OperationalFinanceAccount entity <-> domain model."""
    
    @staticmethod
    def to_domain(entity: OperationalAccountEntity) -> OperationalFinanceAccount:
        """Convert entity to domain model."""
        return OperationalFinanceAccount(
            id=entity.id,
            name=entity.name,
            details=entity.details,
            account_number=entity.account_number,
            account_type=entity.account_type,
            currency=entity.currency,
            start_balance=entity.start_balance,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_deleted=entity.is_deleted,
            text_color=entity.text_color,
            bg_color=entity.bg_color,
            sort_position=entity.sort_position,
        )
    
    @staticmethod
    def to_entity(model: OperationalFinanceAccount) -> OperationalAccountEntity:
        """Convert domain model to entity."""
        entity = OperationalAccountEntity(
            name=model.name,
            details=model.details,
            account_number=model.account_number,
            account_type=model.account_type,
            currency=model.currency,
            start_balance=model.start_balance,
            is_active=model.is_active,
            text_color=model.text_color,
            bg_color=model.bg_color,
            sort_position=model.sort_position,
        )
        
        if model.id is not None:
            entity.id = model.id
            entity.created_at = model.created_at
            entity.updated_at = model.updated_at
            entity.is_deleted = model.is_deleted
        
        return entity


class OperationalFinanceTransactionMapper:
    """Mapper for OperationalFinanceTransaction entity <-> domain model."""
    
    @staticmethod
    def to_domain(entity: OperationalTransactionEntity) -> OperationalFinanceTransaction:
        """Convert entity to domain model."""
        return OperationalFinanceTransaction(
            id=entity.id,
            transaction_number=entity.transaction_number,
            transaction_type=entity.transaction_type,
            status=entity.status,
            amount=entity.amount,
            currency=entity.currency,
            description=entity.description,
            comment=entity.comment,
            transaction_date=entity.transaction_date,
            account_id=entity.account_id,
            category_id=entity.category_id,
            related_transaction_id=entity.related_transaction_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_deleted=entity.is_deleted,
            text_color=getattr(entity, 'text_color', None),
            bg_color=getattr(entity, 'bg_color', None),
            sort_position=getattr(entity, 'sort_position', None),
        )
    
    @staticmethod
    def to_entity(model: OperationalFinanceTransaction) -> OperationalTransactionEntity:
        """Convert domain model to entity."""
        entity = OperationalTransactionEntity(
            transaction_number=model.transaction_number,
            transaction_type=model.transaction_type,
            status=model.status,
            amount=model.amount,
            currency=model.currency,
            description=model.description,
            comment=model.comment,
            transaction_date=model.transaction_date,
            account_id=model.account_id,
            category_id=model.category_id,
            related_transaction_id=model.related_transaction_id,
        )
        
        if model.id is not None:
            entity.id = model.id
            entity.created_at = model.created_at
            entity.updated_at = model.updated_at
            entity.is_deleted = model.is_deleted
        
        return entity


class OperationalTransactionCategoryMapper:
    """Mapper for OperationalTransactionCategory entity <-> domain model."""
    
    @staticmethod
    def to_domain(entity: OperationalCategoryEntity, parent_id: int | None = None) -> OperationalTransactionCategory:
        """Convert entity to domain model.
        
        Args:
            entity: Category entity from database
            parent_id: Parent category ID (from closure table, if applicable)
        """
        return OperationalTransactionCategory(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            parent_id=parent_id,  # This comes from closure table query
            icon=entity.icon,
            text_color=entity.text_color,
            bg_color=entity.bg_color,
            sort_position=entity.sort_position,
            is_active=entity.is_active,
            is_system=entity.is_system,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_deleted=entity.is_deleted,
        )
    
    @staticmethod
    def to_entity(model: OperationalTransactionCategory) -> OperationalCategoryEntity:
        """Convert domain model to entity.
        
        Note: parent_id is NOT stored in entity directly, 
        it should be managed through OperationalCategoryTreeEntity separately.
        """
        entity = OperationalCategoryEntity(
            name=model.name,
            description=model.description,
            icon=model.icon,
            text_color=model.text_color,
            bg_color=model.bg_color,
            sort_position=model.sort_position,
            is_active=model.is_active,
            is_system=model.is_system,
        )
        
        if model.id is not None:
            entity.id = model.id
            entity.created_at = model.created_at
            entity.updated_at = model.updated_at
            entity.is_deleted = model.is_deleted
        
        return entity
