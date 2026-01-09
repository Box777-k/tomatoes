"""Operational transaction status enums."""

from enum import Enum


class OperationalTransactionStatus(str, Enum):
    """Статус операционной финансовой операции."""
    
    ACTIVE = "Активная"
    CANCELLED = "Отменена"
    PENDING = "Ожидает подтверждения"
