"""Finance repositories."""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.entities import (
    OperationalAccountEntity,
    OperationalTransactionEntity,
    OperationalCategoryEntity,
    OperationalCategoryTreeEntity,
)
from app.modules.finance.enums import OperationalTransactionType, OperationalTransactionStatus
from .mappers import (
    OperationalFinanceAccountMapper,
    OperationalFinanceTransactionMapper,
    OperationalTransactionCategoryMapper,
)
from .models import (
    OperationalFinanceAccount,
    OperationalFinanceTransaction,
    OperationalTransactionCategory,
)


class OperationalFinanceAccountRepository:
    """Repository for operational finance accounts."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.mapper = OperationalFinanceAccountMapper()
    
    async def get_by_id(self, account_id: int) -> Optional[OperationalFinanceAccount]:
        """Get account by ID."""
        stmt = select(OperationalAccountEntity).where(
            and_(
                OperationalAccountEntity.id == account_id,
                OperationalAccountEntity.is_deleted == False
            )
        )
        result = await self.session.execute(stmt)
        entity = result.scalar_one_or_none()
        
        return self.mapper.to_domain(entity) if entity else None
    
    async def get_all(self, include_inactive: bool = False) -> list[OperationalFinanceAccount]:
        """Get all accounts."""
        conditions = [OperationalAccountEntity.is_deleted == False]
        
        if not include_inactive:
            conditions.append(OperationalAccountEntity.is_active == True)
        
        stmt = select(OperationalAccountEntity).where(and_(*conditions)).order_by(
            OperationalAccountEntity.sort_position.asc(),
            OperationalAccountEntity.name.asc()
        )
        result = await self.session.execute(stmt)
        entities = result.scalars().all()
        
        return [self.mapper.to_domain(entity) for entity in entities]
    
    async def get_active(self) -> list[OperationalFinanceAccount]:
        """Get only active accounts."""
        return await self.get_all(include_inactive=False)
    
    async def create(self, account: OperationalFinanceAccount) -> OperationalFinanceAccount:
        """Create new account."""
        entity = self.mapper.to_entity(account)
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        
        return self.mapper.to_domain(entity)
    
    async def update(self, account: OperationalFinanceAccount) -> OperationalFinanceAccount:
        """Update existing account."""
        entity = await self.session.get(OperationalAccountEntity, account.id)
        if not entity:
            raise ValueError(f"Account with id {account.id} not found")
        
        # Update fields
        entity.name = account.name
        entity.details = account.details
        entity.account_number = account.account_number
        entity.account_type = account.account_type
        entity.currency = account.currency
        entity.start_balance = account.start_balance
        entity.is_active = account.is_active
        entity.text_color = account.text_color
        entity.bg_color = account.bg_color
        entity.sort_position = account.sort_position
        entity.updated_at = datetime.utcnow()
        
        await self.session.flush()
        await self.session.refresh(entity)
        
        return self.mapper.to_domain(entity)
    
    async def delete(self, account_id: int) -> bool:
        """Soft delete account."""
        entity = await self.session.get(OperationalAccountEntity, account_id)
        if not entity:
            return False
        
        entity.is_deleted = True
        entity.updated_at = datetime.utcnow()
        await self.session.flush()
        
        return True
    
    async def get_with_balance(self, account_id: int, as_of_date: Optional[date] = None) -> tuple[OperationalFinanceAccount, Decimal]:
        """Get account with calculated balance."""
        account = await self.get_by_id(account_id)
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        
        balance = await self.get_account_balance(account_id, as_of_date)
        
        return account, balance
    
    async def get_account_balance(self, account_id: int, as_of_date: Optional[date] = None) -> Decimal:
        """Calculate account balance as of specific date."""
        # Get account to get start_balance
        account = await self.get_by_id(account_id)
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        
        # Build query for transactions
        conditions = [
            OperationalTransactionEntity.account_id == account_id,
            OperationalTransactionEntity.status == OperationalTransactionStatus.ACTIVE,
            OperationalTransactionEntity.is_deleted == False,
        ]
        
        if as_of_date:
            conditions.append(OperationalTransactionEntity.transaction_date <= as_of_date)
        
        # Sum income transactions
        stmt_income = select(func.coalesce(func.sum(OperationalTransactionEntity.amount), 0)).where(
            and_(
                *conditions,
                OperationalTransactionEntity.transaction_type == OperationalTransactionType.INCOME
            )
        )
        result_income = await self.session.execute(stmt_income)
        total_income = result_income.scalar() or Decimal(0)
        
        # Sum expense transactions
        stmt_expense = select(func.coalesce(func.sum(OperationalTransactionEntity.amount), 0)).where(
            and_(
                *conditions,
                OperationalTransactionEntity.transaction_type == OperationalTransactionType.EXPENSE
            )
        )
        result_expense = await self.session.execute(stmt_expense)
        total_expense = result_expense.scalar() or Decimal(0)
        
        # Calculate balance: start_balance + income - expense
        balance = account.start_balance + total_income - total_expense
        
        return balance


class OperationalFinanceTransactionRepository:
    """Repository for operational finance transactions."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.mapper = OperationalFinanceTransactionMapper()
    
    async def get_by_id(self, transaction_id: int) -> Optional[OperationalFinanceTransaction]:
        """Get transaction by ID."""
        stmt = select(OperationalTransactionEntity).where(
            and_(
                OperationalTransactionEntity.id == transaction_id,
                OperationalTransactionEntity.is_deleted == False
            )
        )
        result = await self.session.execute(stmt)
        entity = result.scalar_one_or_none()
        
        return self.mapper.to_domain(entity) if entity else None
    
    async def get_by_account(
        self,
        account_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> list[OperationalFinanceTransaction]:
        """Get transactions by account."""
        stmt = select(OperationalTransactionEntity).where(
            and_(
                OperationalTransactionEntity.account_id == account_id,
                OperationalTransactionEntity.is_deleted == False
            )
        ).order_by(
            OperationalTransactionEntity.transaction_date.desc(),
            OperationalTransactionEntity.created_at.desc()
        )
        
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)
        
        result = await self.session.execute(stmt)
        entities = result.scalars().all()
        
        return [self.mapper.to_domain(entity) for entity in entities]
    
    async def get_by_period(
        self,
        date_from: date,
        date_to: date,
        account_id: Optional[int] = None,
        transaction_type: Optional[OperationalTransactionType] = None
    ) -> list[OperationalFinanceTransaction]:
        """Get transactions by period with optional filters."""
        conditions = [
            OperationalTransactionEntity.transaction_date >= date_from,
            OperationalTransactionEntity.transaction_date <= date_to,
            OperationalTransactionEntity.is_deleted == False
        ]
        
        if account_id:
            conditions.append(OperationalTransactionEntity.account_id == account_id)
        
        if transaction_type:
            conditions.append(OperationalTransactionEntity.transaction_type == transaction_type)
        
        stmt = select(OperationalTransactionEntity).where(
            and_(*conditions)
        ).order_by(
            OperationalTransactionEntity.transaction_date.asc(),
            OperationalTransactionEntity.created_at.asc()
        )
        
        result = await self.session.execute(stmt)
        entities = result.scalars().all()
        
        return [self.mapper.to_domain(entity) for entity in entities]
    
    async def create(self, transaction: OperationalFinanceTransaction) -> OperationalFinanceTransaction:
        """Create new transaction."""
        entity = self.mapper.to_entity(transaction)
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        
        return self.mapper.to_domain(entity)
    
    async def update(self, transaction: OperationalFinanceTransaction) -> OperationalFinanceTransaction:
        """Update existing transaction."""
        entity = await self.session.get(OperationalTransactionEntity, transaction.id)
        if not entity:
            raise ValueError(f"Transaction with id {transaction.id} not found")
        
        # Update allowed fields (not all fields should be updatable)
        entity.description = transaction.description
        entity.category_id = transaction.category_id
        entity.transaction_date = transaction.transaction_date
        entity.updated_at = datetime.utcnow()
        
        await self.session.flush()
        await self.session.refresh(entity)
        
        return self.mapper.to_domain(entity)
    
    async def cancel(self, transaction_id: int) -> OperationalFinanceTransaction:
        """Cancel transaction."""
        entity = await self.session.get(OperationalTransactionEntity, transaction_id)
        if not entity:
            raise ValueError(f"Transaction with id {transaction_id} not found")
        
        if entity.status != OperationalTransactionStatus.ACTIVE:
            raise ValueError("Only active transactions can be cancelled")
        
        entity.status = OperationalTransactionStatus.CANCELLED
        entity.updated_at = datetime.utcnow()
        
        await self.session.flush()
        await self.session.refresh(entity)
        
        return self.mapper.to_domain(entity)
    
    async def create_transfer(
        self,
        source_transaction: OperationalFinanceTransaction,
        destination_transaction: OperationalFinanceTransaction
    ) -> tuple[OperationalFinanceTransaction, OperationalFinanceTransaction]:
        """Create pair of linked transactions for transfer between accounts."""
        # Create source (expense) transaction
        source_entity = self.mapper.to_entity(source_transaction)
        self.session.add(source_entity)
        await self.session.flush()
        await self.session.refresh(source_entity)
        
        # Create destination (income) transaction with link to source
        destination_entity = self.mapper.to_entity(destination_transaction)
        destination_entity.related_transaction_id = source_entity.id
        self.session.add(destination_entity)
        await self.session.flush()
        await self.session.refresh(destination_entity)
        
        # Update source with link to destination
        source_entity.related_transaction_id = destination_entity.id
        await self.session.flush()
        await self.session.refresh(source_entity)
        
        return (
            self.mapper.to_domain(source_entity),
            self.mapper.to_domain(destination_entity)
        )


class OperationalTransactionCategoryRepository:
    """Repository for operational transaction categories."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.mapper = OperationalTransactionCategoryMapper()
    
    async def get_by_id(self, category_id: int) -> Optional[OperationalTransactionCategory]:
        """Get category by ID."""
        stmt = select(OperationalCategoryEntity).where(
            and_(
                OperationalCategoryEntity.id == category_id,
                OperationalCategoryEntity.is_deleted == False
            )
        )
        result = await self.session.execute(stmt)
        entity = result.scalar_one_or_none()
        
        if not entity:
            return None
        
        # Get parent_id from closure table (level = 1 means direct parent)
        parent_stmt = select(OperationalCategoryTreeEntity.parent_category_id).where(
            and_(
                OperationalCategoryTreeEntity.child_category_id == category_id,
                OperationalCategoryTreeEntity.level == 1
            )
        )
        parent_result = await self.session.execute(parent_stmt)
        parent_id = parent_result.scalar_one_or_none()
        
        return self.mapper.to_domain(entity, parent_id)
    
    async def get_all(self, include_inactive: bool = False) -> list[OperationalTransactionCategory]:
        """Get all categories."""
        conditions = [OperationalCategoryEntity.is_deleted == False]
        
        if not include_inactive:
            conditions.append(OperationalCategoryEntity.is_active == True)
        
        stmt = select(OperationalCategoryEntity).where(and_(*conditions)).order_by(
            OperationalCategoryEntity.sort_position.asc(),
            OperationalCategoryEntity.name.asc()
        )
        result = await self.session.execute(stmt)
        entities = result.scalars().all()
        
        # For each category, get parent_id from closure table
        categories = []
        for entity in entities:
            parent_stmt = select(OperationalCategoryTreeEntity.parent_category_id).where(
                and_(
                    OperationalCategoryTreeEntity.child_category_id == entity.id,
                    OperationalCategoryTreeEntity.level == 1
                )
            )
            parent_result = await self.session.execute(parent_stmt)
            parent_id = parent_result.scalar_one_or_none()
            
            categories.append(self.mapper.to_domain(entity, parent_id))
        
        return categories
    
    async def get_tree(self) -> list[OperationalTransactionCategory]:
        """Get category tree (root categories with children)."""
        # For now, return all categories (tree building can be done in service)
        return await self.get_all()
    
    async def create(
        self,
        category: OperationalTransactionCategory,
        parent_id: Optional[int] = None
    ) -> OperationalTransactionCategory:
        """Create new category."""
        entity = self.mapper.to_entity(category)
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        
        # If there's a parent, create closure table entries
        if parent_id:
            await self._create_closure_entries(entity.id, parent_id)
        
        return self.mapper.to_domain(entity, parent_id)
    
    async def update(self, category: OperationalTransactionCategory) -> OperationalTransactionCategory:
        """Update existing category."""
        entity = await self.session.get(OperationalCategoryEntity, category.id)
        if not entity:
            raise ValueError(f"Category with id {category.id} not found")
        
        # Update fields
        entity.name = category.name
        entity.description = category.description
        entity.icon = category.icon
        entity.text_color = category.text_color
        entity.bg_color = category.bg_color
        entity.sort_position = category.sort_position
        entity.is_active = category.is_active
        # Note: is_system cannot be changed
        entity.updated_at = datetime.utcnow()
        
        await self.session.flush()
        await self.session.refresh(entity)
        
        return self.mapper.to_domain(entity, category.parent_id)
    
    async def delete(self, category_id: int) -> bool:
        """Soft delete category."""
        entity = await self.session.get(OperationalCategoryEntity, category_id)
        if not entity:
            return False
        
        if entity.is_system:
            raise ValueError("System categories cannot be deleted")
        
        entity.is_deleted = True
        entity.updated_at = datetime.utcnow()
        await self.session.flush()
        
        return True
    
    async def get_with_children(self, category_id: int) -> tuple[OperationalTransactionCategory, list[OperationalTransactionCategory]]:
        """Get category with its direct children."""
        category = await self.get_by_id(category_id)
        if not category:
            raise ValueError(f"Category with id {category_id} not found")
        
        # Get children from closure table (level = 1 means direct children)
        stmt = select(OperationalCategoryEntity).join(
            OperationalCategoryTreeEntity,
            OperationalCategoryEntity.id == OperationalCategoryTreeEntity.child_category_id
        ).where(
            and_(
                OperationalCategoryTreeEntity.parent_category_id == category_id,
                OperationalCategoryTreeEntity.level == 1,
                OperationalCategoryEntity.is_deleted == False
            )
        ).order_by(
            OperationalCategoryEntity.sort_position.asc(),
            OperationalCategoryEntity.name.asc()
        )
        
        result = await self.session.execute(stmt)
        child_entities = result.scalars().all()
        
        children = [self.mapper.to_domain(entity, category_id) for entity in child_entities]
        
        return category, children
    
    async def _create_closure_entries(self, child_id: int, parent_id: int) -> None:
        """Create closure table entries for new category relationship."""
        # Get all ancestors of parent
        stmt = select(
            OperationalCategoryTreeEntity.parent_category_id,
            OperationalCategoryTreeEntity.level
        ).where(
            OperationalCategoryTreeEntity.child_category_id == parent_id
        )
        result = await self.session.execute(stmt)
        ancestors = result.all()
        
        # Create entry for direct parent
        direct_entry = OperationalCategoryTreeEntity(
            parent_category_id=parent_id,
            child_category_id=child_id,
            level=1
        )
        self.session.add(direct_entry)
        
        # Create entries for all ancestors
        for ancestor_id, ancestor_level in ancestors:
            ancestor_entry = OperationalCategoryTreeEntity(
                parent_category_id=ancestor_id,
                child_category_id=child_id,
                level=ancestor_level + 1
            )
            self.session.add(ancestor_entry)
        
        await self.session.flush()


class OperationalTransactionCategoryTreeRepository:
    """Repository for operational transaction category tree (closure table)."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_ancestors(self, category_id: int) -> list[tuple[int, int]]:
        """Get all ancestors of a category with their levels.
        
        Returns:
            List of tuples (ancestor_id, level) ordered by level ascending
        """
        stmt = select(
            OperationalCategoryTreeEntity.parent_category_id,
            OperationalCategoryTreeEntity.level
        ).where(
            OperationalCategoryTreeEntity.child_category_id == category_id
        ).order_by(
            OperationalCategoryTreeEntity.level.asc()
        )
        
        result = await self.session.execute(stmt)
        return result.all()
    
    async def get_descendants(self, category_id: int) -> list[tuple[int, int]]:
        """Get all descendants of a category with their levels.
        
        Returns:
            List of tuples (descendant_id, level) ordered by level ascending
        """
        stmt = select(
            OperationalCategoryTreeEntity.child_category_id,
            OperationalCategoryTreeEntity.level
        ).where(
            OperationalCategoryTreeEntity.parent_category_id == category_id
        ).order_by(
            OperationalCategoryTreeEntity.level.asc()
        )
        
        result = await self.session.execute(stmt)
        return result.all()
    
    async def get_parent_id(self, category_id: int) -> Optional[int]:
        """Get direct parent ID of a category (level = 1)."""
        stmt = select(OperationalCategoryTreeEntity.parent_category_id).where(
            and_(
                OperationalCategoryTreeEntity.child_category_id == category_id,
                OperationalCategoryTreeEntity.level == 1
            )
        )
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_children_ids(self, category_id: int) -> list[int]:
        """Get direct children IDs of a category (level = 1)."""
        stmt = select(OperationalCategoryTreeEntity.child_category_id).where(
            and_(
                OperationalCategoryTreeEntity.parent_category_id == category_id,
                OperationalCategoryTreeEntity.level == 1
            )
        )
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_root_category_ids(self) -> list[int]:
        """Get all root categories (categories without parents)."""
        # Categories that are not in child_category_id of closure table are roots
        stmt = select(OperationalCategoryEntity.id).where(
            and_(
                OperationalCategoryEntity.is_deleted == False,
                ~OperationalCategoryEntity.id.in_(
                    select(OperationalCategoryTreeEntity.child_category_id)
                )
            )
        ).order_by(
            OperationalCategoryEntity.sort_position.asc(),
            OperationalCategoryEntity.name.asc()
        )
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def create_relationship(self, parent_id: int, child_id: int) -> None:
        """Create parent-child relationship in closure table.
        
        This creates entries for:
        1. Direct parent-child relationship (level=1)
        2. Relationships with all ancestors of parent
        """
        if parent_id == child_id:
            raise ValueError("Category cannot be its own parent")
        
        # Check if relationship already exists
        existing_stmt = select(OperationalCategoryTreeEntity).where(
            and_(
                OperationalCategoryTreeEntity.parent_category_id == parent_id,
                OperationalCategoryTreeEntity.child_category_id == child_id,
                OperationalCategoryTreeEntity.level == 1
            )
        )
        existing = await self.session.execute(existing_stmt)
        if existing.scalar_one_or_none():
            raise ValueError("Relationship already exists")
        
        # Get all ancestors of parent
        ancestors = await self.get_ancestors(parent_id)
        
        # Create entry for direct parent
        direct_entry = OperationalCategoryTreeEntity(
            parent_category_id=parent_id,
            child_category_id=child_id,
            level=1
        )
        self.session.add(direct_entry)
        
        # Create entries for all ancestors
        for ancestor_id, ancestor_level in ancestors:
            ancestor_entry = OperationalCategoryTreeEntity(
                parent_category_id=ancestor_id,
                child_category_id=child_id,
                level=ancestor_level + 1
            )
            self.session.add(ancestor_entry)
        
        await self.session.flush()
    
    async def delete_relationship(self, parent_id: int, child_id: int) -> bool:
        """Delete parent-child relationship from closure table.
        
        This removes all entries related to this relationship,
        including cascaded ancestor relationships.
        """
        # Delete all entries where child_id is the child
        from sqlalchemy import delete
        
        stmt = delete(OperationalCategoryTreeEntity).where(
            OperationalCategoryTreeEntity.child_category_id == child_id
        )
        
        result = await self.session.execute(stmt)
        await self.session.flush()
        
        return result.rowcount > 0
    
    async def move_category(self, category_id: int, new_parent_id: Optional[int]) -> None:
        """Move category to a new parent.
        
        This removes old relationships and creates new ones.
        """
        # Delete existing relationships
        await self.delete_relationship(0, category_id)  # parent_id=0 means delete all
        
        # Create new relationships if new_parent_id is provided
        if new_parent_id:
            await self.create_relationship(new_parent_id, category_id)
        
        await self.session.flush()
    
    async def get_path(self, category_id: int) -> list[int]:
        """Get full path from root to category.
        
        Returns:
            List of category IDs from root to the given category (inclusive)
        """
        ancestors = await self.get_ancestors(category_id)
        
        # Build path from root to category
        path = [ancestor_id for ancestor_id, _ in reversed(ancestors)]
        path.append(category_id)
        
        return path
    
    async def get_level(self, category_id: int) -> int:
        """Get level of category in tree (0 for root categories)."""
        # Count how many ancestors the category has
        stmt = select(func.count()).where(
            OperationalCategoryTreeEntity.child_category_id == category_id
        )
        
        result = await self.session.execute(stmt)
        return result.scalar() or 0
