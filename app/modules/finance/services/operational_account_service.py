"""Operational finance account service."""

from datetime import date
from decimal import Decimal
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories import OperationalFinanceAccountRepository
from ..models import OperationalFinanceAccount


class OperationalFinanceAccountService:
    """Service for operational finance account business logic."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.account_repo = OperationalFinanceAccountRepository(session)
    
    async def create_account(self, account: OperationalFinanceAccount) -> OperationalFinanceAccount:
        """Create new operational account.
        
        Business rules:
        - Account number must be unique if provided
        - Start balance cannot be negative
        """
        if account.start_balance < 0:
            raise ValueError("Start balance cannot be negative")
        
        return await self.account_repo.create(account)
    
    async def update_account(self, account: OperationalFinanceAccount) -> OperationalFinanceAccount:
        """Update existing operational account.
        
        Business rules:
        - Cannot change account_type after creation
        - Cannot change start_balance if transactions exist
        """
        return await self.account_repo.update(account)
    
    async def activate_account(self, account_id: int) -> OperationalFinanceAccount:
        """Activate account."""
        account = await self.account_repo.get_by_id(account_id)
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        
        account.activate()
        return await self.account_repo.update(account)
    
    async def deactivate_account(self, account_id: int) -> OperationalFinanceAccount:
        """Deactivate account.
        
        Business rules:
        - Deactivated accounts cannot have new transactions
        - Existing transactions remain visible
        """
        account = await self.account_repo.get_by_id(account_id)
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        
        account.deactivate()
        return await self.account_repo.update(account)
    
    async def get_account_with_balance(
        self,
        account_id: int,
        as_of_date: Optional[date] = None
    ) -> tuple[OperationalFinanceAccount, Decimal]:
        """Get account with calculated balance.
        
        Includes deactivated accounts (they can still have balance).
        """
        return await self.account_repo.get_with_balance(account_id, as_of_date)
    
    async def get_account_history(
        self,
        account_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> list:
        """Get account transaction history.
        
        Includes transactions even if account is deactivated.
        """
        from ..repositories import OperationalFinanceTransactionRepository
        
        transaction_repo = OperationalFinanceTransactionRepository(self.session)
        return await transaction_repo.get_by_account(account_id, limit, offset)
    
    async def get_all_accounts(self, include_inactive: bool = False) -> list[OperationalFinanceAccount]:
        """Get all accounts with optional filter for inactive."""
        return await self.account_repo.get_all(include_inactive)
    
    async def get_active_accounts(self) -> list[OperationalFinanceAccount]:
        """Get only active accounts."""
        return await self.account_repo.get_active()
