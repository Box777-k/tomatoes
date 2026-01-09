"""Operational account entity."""

from sqlalchemy import Column, String, Numeric, Boolean, Enum as SQLEnum
from app.enums import OperationalAccountType
from .base import BaseEntity


class OperationalAccountEntity(BaseEntity):
    """Operational account table."""
    
    __tablename__ = "operational_accounts"
    __table_args__ = {'comment': 'Операционные счета организации (банковские, кассовые и прочие счета)'}
    
    name = Column(String(200), nullable=False, comment="Наименование счета")
    details = Column(String, nullable=True, comment="Дополнительная информация о счете")
    account_number = Column(String(100), unique=True, nullable=True, index=True, comment="Номер счета")
    account_type = Column(SQLEnum(OperationalAccountType), nullable=False, comment="Тип счета")
    currency = Column(String(4), nullable=False, default="RUB", comment="Валюта счета (код ISO 4217)")
    start_balance = Column(Numeric(12, 2), nullable=False, default=0, comment="Начальный остаток на счете")
    is_active = Column(Boolean, nullable=False, default=True, comment="Признак активности счета")
