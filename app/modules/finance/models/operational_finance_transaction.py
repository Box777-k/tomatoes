"""Operational finance transaction domain model."""

from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from app.modules.finance import OperationalTransactionType, OperationalTransactionStatus


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
    order_id: int | None
    movement_id: int | None
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    text_color: str | None
    bg_color: str | None
    sort_position: int | None
    
    def cancel(self) -> None:
        """Cancel transaction."""
        self.status = OperationalTransactionStatus.CANCELLED
    
    def is_cancelled(self) -> bool:
        """Check if transaction is cancelled."""
        return self.status == OperationalTransactionStatus.CANCELLED
    
    def is_transfer(self) -> bool:
        """Check if transaction is part of a transfer."""
        return self.related_transaction_id is not None
