"""Operational account enums."""

from enum import Enum


class OperationalAccountType(str, Enum):
    """Тип операционного счета."""
    
    BANK = "Банковский счет"
    CASH = "Касса"
    OTHER = "Прочие счета"
