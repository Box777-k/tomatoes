"""Operational transaction enums."""

from enum import Enum


class OperationalTransactionType(str, Enum):
    """Тип операционной финансовой операции."""
    
    INCOME = "Доход"
    EXPENSE = "Расход"
