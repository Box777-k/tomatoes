"""Finance balance calculation service."""

from datetime import date, timedelta
from decimal import Decimal
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories import (
    OperationalFinanceAccountRepository,
    OperationalFinanceTransactionRepository,
)
from ..models import OperationalFinanceAccount


class FinanceBalanceService:
    """Service for balance calculations and reporting."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.account_repo = OperationalFinanceAccountRepository(session)
        self.transaction_repo = OperationalFinanceTransactionRepository(session)
    
    async def calculate_account_balance(
        self,
        account_id: int,
        as_of_date: Optional[date] = None
    ) -> Decimal:
        """Calculate account balance as of specific date.
        
        Formula: start_balance + total_income - total_expense
        """
        return await self.account_repo.get_account_balance(account_id, as_of_date)
    
    async def calculate_all_balances(
        self,
        as_of_date: Optional[date] = None,
        include_inactive: bool = False
    ) -> dict[int, Decimal]:
        """Calculate balances for all accounts.
        
        Returns:
            Dictionary mapping account_id to balance
        """
        accounts = await self.account_repo.get_all(include_inactive)
        
        balances = {}
        for account in accounts:
            balance = await self.calculate_account_balance(account.id, as_of_date)
            balances[account.id] = balance
        
        return balances
    
    async def get_balance_history(
        self,
        account_id: int,
        date_from: date,
        date_to: date,
        interval_days: int = 1
    ) -> list[tuple[date, Decimal]]:
        """Get balance history for period.
        
        Returns list of (date, balance) tuples for each interval.
        
        Args:
            account_id: Account to calculate balance for
            date_from: Start date
            date_to: End date
            interval_days: Days between balance calculations (default 1 = daily)
        """
        if date_from > date_to:
            raise ValueError("date_from must be before date_to")
        
        history = []
        current_date = date_from
        
        while current_date <= date_to:
            balance = await self.calculate_account_balance(account_id, current_date)
            history.append((current_date, balance))
            current_date += timedelta(days=interval_days)
        
        return history
    
    async def get_total_balance(
        self,
        as_of_date: Optional[date] = None,
        currency: str = "RUB"
    ) -> Decimal:
        """Get total balance across all active accounts in specific currency.
        
        Args:
            as_of_date: Date to calculate balance for (None = today)
            currency: Currency to filter by (default RUB)
        """
        accounts = await self.account_repo.get_active()
        
        # Filter by currency
        currency_accounts = [a for a in accounts if a.currency == currency]
        
        total = Decimal(0)
        for account in currency_accounts:
            balance = await self.calculate_account_balance(account.id, as_of_date)
            total += balance
        
        return total
    
    async def get_account_summary(
        self,
        account_id: int,
        date_from: date,
        date_to: date
    ) -> dict:
        """Get account summary for period.
        
        Returns:
            Dictionary with opening balance, closing balance,
            total income, total expense, and transaction count
        """
        account = await self.account_repo.get_by_id(account_id)
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        
        # Get transactions for period
        transactions = await self.transaction_repo.get_by_period(
            date_from,
            date_to,
            account_id=account_id
        )
        
        # Calculate totals
        from ..enums import OperationalTransactionType, OperationalTransactionStatus
        
        total_income = sum(
            t.amount for t in transactions
            if t.transaction_type == OperationalTransactionType.INCOME
            and t.status == OperationalTransactionStatus.ACTIVE
        )
        
        total_expense = sum(
            t.amount for t in transactions
            if t.transaction_type == OperationalTransactionType.EXPENSE
            and t.status == OperationalTransactionStatus.ACTIVE
        )
        
        # Get balances
        opening_balance = await self.calculate_account_balance(
            account_id,
            date_from - timedelta(days=1)
        )
        closing_balance = await self.calculate_account_balance(account_id, date_to)
        
        return {
            "account": account,
            "period": {
                "date_from": date_from,
                "date_to": date_to
            },
            "opening_balance": opening_balance,
            "closing_balance": closing_balance,
            "total_income": total_income,
            "total_expense": total_expense,
            "net_change": total_income - total_expense,
            "transaction_count": len(transactions),
            "transactions": transactions
        }
    
    async def get_multi_account_summary(
        self,
        date_from: date,
        date_to: date,
        account_ids: Optional[list[int]] = None
    ) -> list[dict]:
        """Get summary for multiple accounts.
        
        Args:
            date_from: Start date
            date_to: End date
            account_ids: List of account IDs (None = all active accounts)
        """
        # Get accounts
        if account_ids:
            accounts = []
            for acc_id in account_ids:
                account = await self.account_repo.get_by_id(acc_id)
                if account:
                    accounts.append(account)
        else:
            accounts = await self.account_repo.get_active()
        
        # Get summary for each account
        summaries = []
        for account in accounts:
            summary = await self.get_account_summary(account.id, date_from, date_to)
            summaries.append(summary)
        
        return summaries
