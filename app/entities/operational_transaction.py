"""Operational transaction entity."""

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, Enum as SQLEnum
from app.enums import OperationalTransactionType, OperationalTransactionStatus
from .base import BaseEntity


class OperationalTransactionEntity(BaseEntity):
    """Operational financial transaction table."""
    
    __tablename__ = "operational_transactions"
    __table_args__ = {'comment': 'Операционные финансовые операции организации'}
    
    transaction_number = Column(String(50), unique=True, nullable=False, index=True, comment="Номер финансовой операции")
    transaction_type = Column(SQLEnum(OperationalTransactionType), nullable=False, index=True, comment="Тип операции")
    status = Column(SQLEnum(OperationalTransactionStatus), nullable=False, default=OperationalTransactionStatus.ACTIVE, index=True, comment="Статус операции")
    amount = Column(Numeric(12, 2), nullable=False, comment="Сумма операции")
    currency = Column(String(3), nullable=False, default="RUB", comment="Валюта операции (код ISO 4217)")
    description = Column(String(500), nullable=True, comment="Описание финансовой операции")
    comment = Column(String(500), nullable=True, comment="Автоматический комментарий (переводы, системные операции)")
    transaction_date = Column(Date, nullable=False, index=True, comment="Дата совершения операции")
    
    # Links to other entities
    account_id = Column(Integer, ForeignKey("operational_accounts.id"), nullable=False, index=True, comment="Счет организации")
    category_id = Column(Integer, ForeignKey("operational_categories.id"), nullable=True, index=True, comment="Категория операции")
    related_transaction_id = Column(Integer, ForeignKey("operational_transactions.id"), nullable=True, index=True, comment="Связанная транзакция (для переводов)")
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True, comment="Связь с заказом")
    movement_id = Column(Integer, ForeignKey("movements.id"), nullable=True, comment="Связь с документом перемещения")
