"""Operational finance transaction service."""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories import (
    OperationalFinanceTransactionRepository,
    OperationalFinanceAccountRepository,
    OperationalTransactionCategoryRepository,
)
from ..models import OperationalFinanceTransaction
from ..enums import OperationalTransactionType, OperationalTransactionStatus


class OperationalFinanceTransactionService:
    """Service for operational finance transaction business logic."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.transaction_repo = OperationalFinanceTransactionRepository(session)
        self.account_repo = OperationalFinanceAccountRepository(session)
        self.category_repo = OperationalTransactionCategoryRepository(session)
    
    async def create_income(
        self,
        account_id: int,
        amount: Decimal,
        transaction_date: date,
        description: str,
        currency: str = "RUB",
        category_id: Optional[int] = None,
    ) -> OperationalFinanceTransaction:
        """Create income transaction.
        
        Business rules:
        - Category is optional for income
        - Account must be active
        - Amount must be positive
        """
        # Validate account
        account = await self.account_repo.get_by_id(account_id)
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        
        if not account.is_available_for_transaction():
            raise ValueError("Account is not available for transactions")
        
        # Validate amount
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        # Validate category if provided
        if category_id:
            category = await self.category_repo.get_by_id(category_id)
            if not category:
                raise ValueError(f"Category with id {category_id} not found")
        
        # Generate transaction number
        transaction_number = await self._generate_transaction_number()
        
        # Create transaction
        transaction = OperationalFinanceTransaction(
            id=None,
            transaction_number=transaction_number,
            transaction_type=OperationalTransactionType.INCOME,
            status=OperationalTransactionStatus.ACTIVE,
            amount=amount,
            currency=currency,
            description=description,
            comment=None,
            transaction_date=transaction_date,
            account_id=account_id,
            category_id=category_id,
            related_transaction_id=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_deleted=False,
            text_color=None,
            bg_color=None,
            sort_position=None,
        )
        
        return await self.transaction_repo.create(transaction)
    
    async def create_expense(
        self,
        account_id: int,
        amount: Decimal,
        transaction_date: date,
        description: str,
        category_id: int,
        currency: str = "RUB",
    ) -> OperationalFinanceTransaction:
        """Create expense transaction.
        
        Business rules:
        - Category is REQUIRED for expense
        - Account must be active
        - Amount must be positive
        """
        # Validate account
        account = await self.account_repo.get_by_id(account_id)
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        
        if not account.is_available_for_transaction():
            raise ValueError("Account is not available for transactions")
        
        # Validate amount
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        # Validate category (required for expense)
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            raise ValueError(f"Category with id {category_id} not found")
        
        # Generate transaction number
        transaction_number = await self._generate_transaction_number()
        
        # Create transaction
        transaction = OperationalFinanceTransaction(
            id=None,
            transaction_number=transaction_number,
            transaction_type=OperationalTransactionType.EXPENSE,
            status=OperationalTransactionStatus.ACTIVE,
            amount=amount,
            currency=currency,
            description=description,
            comment=None,
            transaction_date=transaction_date,
            account_id=account_id,
            category_id=category_id,
            related_transaction_id=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_deleted=False,
            text_color=None,
            bg_color=None,
            sort_position=None,
        )
        
        return await self.transaction_repo.create(transaction)
    
    async def create_transfer(
        self,
        source_account_id: int,
        destination_account_id: int,
        amount: Decimal,
        transaction_date: date,
        description: str,
        currency: str = "RUB",
    ) -> tuple[OperationalFinanceTransaction, OperationalFinanceTransaction]:
        """Create transfer between accounts.
        
        Creates two linked transactions:
        - EXPENSE from source account
        - INCOME to destination account
        
        Business rules:
        - Both accounts must be active
        - Source and destination must be different
        - Amount must be positive
        - Uses system transfer category
        """
        # Validate accounts
        if source_account_id == destination_account_id:
            raise ValueError("Source and destination accounts must be different")
        
        source_account = await self.account_repo.get_by_id(source_account_id)
        if not source_account:
            raise ValueError(f"Source account with id {source_account_id} not found")
        
        destination_account = await self.account_repo.get_by_id(destination_account_id)
        if not destination_account:
            raise ValueError(f"Destination account with id {destination_account_id} not found")
        
        if not source_account.is_available_for_transaction():
            raise ValueError("Source account is not available for transactions")
        
        if not destination_account.is_available_for_transaction():
            raise ValueError("Destination account is not available for transactions")
        
        # Validate amount
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        # Get system transfer category
        from .operational_category_service import OperationalTransactionCategoryService
        category_service = OperationalTransactionCategoryService(self.session)
        transfer_category = await category_service.get_system_transfer_category()
        
        if not transfer_category:
            raise ValueError("System transfer category not found")
        
        # Generate transaction numbers
        source_number = await self._generate_transaction_number()
        dest_number = await self._generate_transaction_number()
        
        # Create source transaction (expense)
        source_transaction = OperationalFinanceTransaction(
            id=None,
            transaction_number=source_number,
            transaction_type=OperationalTransactionType.EXPENSE,
            status=OperationalTransactionStatus.ACTIVE,
            amount=amount,
            currency=currency,
            description=description,
            comment=f"Перевод на счет: {destination_account.name}",
            transaction_date=transaction_date,
            account_id=source_account_id,
            category_id=transfer_category.id,
            related_transaction_id=None,  # Will be set after creation
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_deleted=False,
            text_color=None,
            bg_color=None,
            sort_position=None,
        )
        
        # Create destination transaction (income)
        destination_transaction = OperationalFinanceTransaction(
            id=None,
            transaction_number=dest_number,
            transaction_type=OperationalTransactionType.INCOME,
            status=OperationalTransactionStatus.ACTIVE,
            amount=amount,
            currency=currency,
            description=description,
            comment=f"Перевод со счета: {source_account.name}",
            transaction_date=transaction_date,
            account_id=destination_account_id,
            category_id=transfer_category.id,
            related_transaction_id=None,  # Will be set after creation
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_deleted=False,
            text_color=None,
            bg_color=None,
            sort_position=None,
        )
        
        # Create both transactions with cross-references
        return await self.transaction_repo.create_transfer(
            source_transaction,
            destination_transaction
        )
    
    async def cancel_transaction(self, transaction_id: int) -> OperationalFinanceTransaction:
        """Cancel transaction.
        
        Business rules:
        - If transaction is part of transfer (has related_transaction_id),
          cancel both transactions
        - Only ACTIVE transactions can be cancelled
        """
        transaction = await self.transaction_repo.get_by_id(transaction_id)
        if not transaction:
            raise ValueError(f"Transaction with id {transaction_id} not found")
        
        if not transaction.is_cancellable():
            raise ValueError("Transaction cannot be cancelled")
        
        # Cancel main transaction
        cancelled_transaction = await self.transaction_repo.cancel(transaction_id)
        
        # If this is a transfer, cancel the related transaction too
        if transaction.is_transfer():
            related_transaction = await self.transaction_repo.get_by_id(
                transaction.related_transaction_id
            )
            if related_transaction and related_transaction.is_cancellable():
                await self.transaction_repo.cancel(related_transaction.id)
        
        return cancelled_transaction
    
    async def get_transactions_by_account(
        self,
        account_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> list[OperationalFinanceTransaction]:
        """Get transactions by account.
        
        Includes transactions even if account is deactivated.
        """
        return await self.transaction_repo.get_by_account(account_id, limit, offset)
    
    async def get_transactions_by_period(
        self,
        date_from: date,
        date_to: date,
        account_id: Optional[int] = None,
        transaction_type: Optional[OperationalTransactionType] = None
    ) -> list[OperationalFinanceTransaction]:
        """Get transactions by period with optional filters."""
        return await self.transaction_repo.get_by_period(
            date_from,
            date_to,
            account_id,
            transaction_type
        )
    
    async def _generate_transaction_number(self) -> str:
        """Generate unique transaction number.
        
        Format: TRN-YYYYMMDD-NNNN
        """
        from sqlalchemy import select, func
        from ...entities import OperationalTransactionEntity
        
        today = datetime.utcnow().strftime("%Y%m%d")
        prefix = f"TRN-{today}"
        
        # Get count of transactions today
        stmt = select(func.count()).where(
            OperationalTransactionEntity.transaction_number.like(f"{prefix}%")
        )
        result = await self.session.execute(stmt)
        count = result.scalar() or 0
        
        # Generate number
        return f"{prefix}-{count + 1:04d}"
