"""Pydantic схемы для операционных финансовых транзакций."""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from decimal import Decimal
from app.modules.finance.enums import OperationalTransactionType, OperationalTransactionStatus


class OperationalFinanceTransactionBase(BaseModel):
    """Базовая схема операционной транзакции (общие поля)."""
    
    amount: Decimal = Field(gt=0)  # Сумма операции (должна быть > 0)
    currency: str = Field(default="RUB", max_length=3)  # Валюта (ISO 4217)
    description: str = Field(min_length=1, max_length=500)  # Описание операции (обязательно)
    transaction_date: date  # Дата совершения операции
    account_id: int  # ID счета
    text_color: str | None = Field(None, max_length=7)  # Цвет текста для UI
    bg_color: str | None = Field(None, max_length=7)  # Цвет фона для UI
    sort_position: int | None = None  # Позиция при сортировке


class OperationalFinanceTransactionIncomeCreate(OperationalFinanceTransactionBase):
    """Схема для создания операции поступления денег (INCOME).
    
    Категория опциональна для поступлений.
    """
    
    category_id: int | None = None  # ID категории (опционально для INCOME)


class OperationalFinanceTransactionExpenseCreate(OperationalFinanceTransactionBase):
    """Схема для создания операции расхода денег (EXPENSE).
    
    Категория обязательна для расходов.
    """
    
    category_id: int  # ID категории (обязательно для EXPENSE)


class OperationalFinanceTransactionTransferCreate(BaseModel):
    """Схема для создания перевода между операционными счетами.
    
    Создает две связанные транзакции:
    - EXPENSE со счета-источника
    - INCOME на счет-получатель
    """
    
    amount: Decimal = Field(gt=0)  # Сумма перевода
    currency: str = Field(default="RUB", max_length=3)  # Валюта
    description: str = Field(min_length=1, max_length=500)  # Описание перевода
    transaction_date: date  # Дата перевода
    source_account_id: int  # ID счета списания
    destination_account_id: int  # ID счета зачисления
    
    @field_validator('destination_account_id')
    @classmethod
    def validate_different_accounts(cls, v, info):
        """Проверка что счета разные."""
        if 'source_account_id' in info.data and v == info.data['source_account_id']:
            raise ValueError('Счет-источник и счет-получатель должны быть разными')
        return v


class OperationalFinanceTransactionUpdate(BaseModel):
    """Схема для обновления операционной транзакции (все поля опциональны).
    
    Примечание: изменение transaction_type не допускается.
    """
    
    description: str | None = Field(None, min_length=1, max_length=500)
    category_id: int | None = None
    transaction_date: date | None = None
    text_color: str | None = Field(None, max_length=7)
    bg_color: str | None = Field(None, max_length=7)
    sort_position: int | None = None


class OperationalFinanceTransactionCancelRequest(BaseModel):
    """Схема запроса на отмену операционной транзакции."""
    
    reason: str | None = Field(None, max_length=500)  # Причина отмены (опционально)


class OperationalFinanceTransactionResponse(BaseModel):
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
    order_id: int | None  # ID связанного заказа
    movement_id: int | None  # ID связанного документа перемещения
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
            order_id=getattr(transaction, 'order_id', None),
            movement_id=getattr(transaction, 'movement_id', None),
            text_color=transaction.text_color,
            bg_color=transaction.bg_color,
            sort_position=transaction.sort_position,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at
        )


class OperationalFinanceTransactionListResponse(BaseModel):
    """Схема ответа со списком операционных транзакций."""
    
    transactions: list[OperationalFinanceTransactionResponse]  # Список транзакций
    total: int  # Общее количество
