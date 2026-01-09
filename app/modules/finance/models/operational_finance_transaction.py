"""Operational finance transaction domain model."""

from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from app.modules.finance.enums import OperationalTransactionType, OperationalTransactionStatus


@dataclass
class OperationalFinanceTransaction:
    """Operational finance transaction domain model."""
    
    id: int | None
    transaction_number: str
    transaction_type: OperationalTransactionType
    status: OperationalTransactionStatus
    amount: Decimal
    currency: str
    description: str | None
    comment: str | None
    transaction_date: date
    account_id: int
    category_id: int | None
    related_transaction_id: int | None
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    text_color: str | None
    bg_color: str | None
    sort_position: int | None
    
    def cancel(self) -> None:
        """Cancel transaction."""
        if not self.is_cancellable():
            raise ValueError("Transaction cannot be cancelled")
        self.status = OperationalTransactionStatus.CANCELLED
    
    def is_cancellable(self) -> bool:
        """Check if transaction can be cancelled."""
        return self.status == OperationalTransactionStatus.ACTIVE and not self.is_deleted
    
    def is_cancelled(self) -> bool:
        """Check if transaction is cancelled."""
        return self.status == OperationalTransactionStatus.CANCELLED
    
    def is_transfer(self) -> bool:
        """Check if transaction is part of a transfer between accounts."""
        return self.related_transaction_id is not None
