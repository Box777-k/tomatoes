"""Operational finance account domain model."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from app.modules.finance.enums import OperationalAccountType



@dataclass
class OperationalFinanceAccount:
    """Operational finance account domain model."""
    
    id: int | None
    name: str
    details: str | None
    account_number: str | None
    account_type: OperationalAccountType
    currency: str
    start_balance: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    text_color: str | None
    bg_color: str | None
    sort_position: int | None
    
    def is_available_for_transaction(self) -> bool:
        """Check if account is available for transactions."""
        return self.is_active and not self.is_deleted
    
    def deactivate(self) -> None:
        """Deactivate account."""
        self.is_active = False
