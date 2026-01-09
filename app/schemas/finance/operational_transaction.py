"""Pydantic схемы для операционных финансовых транзакций."""

from pydantic import BaseModel, Field
from datetime import datetime, date
from decimal import Decimal
from app.modules.finance.enums import OperationalTransactionType, OperationalTransactionStatus


class OperationalTransactionBase(BaseModel):
    """Базовая схема операционной транзакции (общие поля для Create)."""
    
    transaction_type: OperationalTransactionType  # Тип операции (INCOME/EXPENSE)
    amount: Decimal = Field(gt=0)  # Сумма операции (должна быть > 0)
    currency: str = Field(default="RUB", max_length=3)  # Валюта (ISO 4217)
    description: str | None = Field(None, max_length=500)  # Описание операции
    comment: str | None = Field(None, max_length=500)  # Автоматический комментарий (для переводов)
    category_id: int | None = None  # ID категории транзакции
    transaction_date: date  # Дата совершения операции
    account_id: int  # ID счета
    text_color: str | None = Field(None, max_length=20)  # Цвет текста для UI
    bg_color: str | None = Field(None, max_length=20)  # Цвет фона для UI
    sort_position: int | None = None  # Позиция при сортировке


class OperationalTransactionCreate(OperationalTransactionBase):
    """Схема для создания новой операционной транзакции."""
    pass


class OperationalTransferCreate(BaseModel):
    """Схема для создания перевода между операционными счетами.
    
    Создает две связанные транзакции:
    - EXPENSE со счета-источника
    - INCOME на счет-получатель
    """
    
    amount: Decimal = Field(gt=0)  # Сумма перевода
    currency: str = Field(default="RUB", max_length=3)  # Валюта
    description: str | None = Field(None, max_length=500)  # Описание перевода
    transaction_date: date  # Дата перевода
    source_account_id: int  # ID счета списания
    destination_account_id: int  # ID счета зачисления


class OperationalTransactionResponse(BaseModel):
    """Схема ответа с данными операционной транзакции."""
    
    id: int  # Идентификатор
    transaction_number: str  # Номер операции (генерируется автоматически)
    transaction_type: OperationalTransactionType  # Тип операции
    status: OperationalTransactionStatus  # Статус (ACTIVE/CANCELLED/PENDING)
    amount: Decimal  # Сумма
    currency: str  # Валюта
    description: str | None  # Описание
    comment: str | None  # Автокомментарий
    category_id: int | None  # ID категории
    transaction_date: date  # Дата операции
    account_id: int  # ID счета
    related_transaction_id: int | None  # ID связанной транзакции (для переводов)
    text_color: str | None  # Цвет текста
    bg_color: str | None  # Цвет фона
    sort_position: int | None  # Позиция сортировки
    created_at: datetime  # Дата создания
    updated_at: datetime  # Дата обновления
    
    @classmethod
    def from_domain(cls, transaction):
        """Создать схему из доменной модели."""
        return cls(
            id=transaction.id,
            transaction_number=transaction.transaction_number,
            transaction_type=transaction.transaction_type,
            status=transaction.status,
            amount=transaction.amount,
            currency=transaction.currency,
            description=transaction.description,
            comment=transaction.comment,
            category_id=transaction.category_id,
            transaction_date=transaction.transaction_date,
            account_id=transaction.account_id,
            related_transaction_id=transaction.related_transaction_id,
            text_color=transaction.text_color,
            bg_color=transaction.bg_color,
            sort_position=transaction.sort_position,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at
        )


class OperationalTransactionListResponse(BaseModel):
    """Схема ответа со списком операционных транзакций."""
    
    transactions: list[OperationalTransactionResponse]  # Список транзакций
    total: int  # Общее количество
