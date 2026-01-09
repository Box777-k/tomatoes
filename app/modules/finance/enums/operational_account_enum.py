"""Operational account enums."""

from enum import Enum


class OperationalAccountType(str, Enum):
    """Тип операционного счета."""
    
    CASH = "cash"
    NON_CASH = "non_cash"
