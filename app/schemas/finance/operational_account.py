"""Pydantic схемы для операционных счетов организации."""

from typing import TYPE_CHECKING
from pydantic import BaseModel, Field
from datetime import datetime, date
from decimal import Decimal
from app.modules.finance.enums import OperationalAccountType

# TYPE_CHECKING - для избежания циклических импортов
# Импорт выполняется только при статической проверке типов, но не в runtime
if TYPE_CHECKING:
    from .operational_transaction import OperationalTransactionResponse


class OperationalAccountBase(BaseModel):
    """Базовая схема операционного счета (общие поля для Create/Update)."""
    
    name: str = Field(min_length=1, max_length=200)  # Название счета
    details: str | None = None  # Дополнительная информация
    account_number: str | None = Field(None, max_length=100)  # Номер счета (расчетный, карты и т.д.)
    account_type: OperationalAccountType  # Тип счета (банк, касса, прочие)
    currency: str = Field(default="RUB", max_length=4)  # Валюта (ISO 4217)
    start_balance: Decimal = Field(default=0, ge=0)  # Начальный остаток
    text_color: str | None = Field(None, max_length=20)  # Цвет текста для UI (hex)
    bg_color: str | None = Field(None, max_length=20)  # Цвет фона для UI (hex)
    sort_position: int | None = None  # Позиция при сортировке


class OperationalAccountCreate(OperationalAccountBase):
    """Схема для создания нового операционного счета."""
    pass


class OperationalAccountUpdate(BaseModel):
    """Схема для обновления операционного счета (все поля опциональны)."""
    
    name: str | None = Field(None, min_length=1, max_length=200)
    details: str | None = None
    account_number: str | None = Field(None, max_length=100)
    account_type: OperationalAccountType | None = None
    currency: str | None = Field(None, max_length=4)
    start_balance: Decimal | None = Field(None, ge=0)
    text_color: str | None = Field(None, max_length=20)
    bg_color: str | None = Field(None, max_length=20)
    sort_position: int | None = None


class OperationalAccountResponse(BaseModel):
    """Схема ответа с данными операционного счета."""
    
    id: int  # Идентификатор
    name: str  # Название
    details: str | None  # Дополнительная информация
    account_number: str | None  # Номер счета
    account_type: OperationalAccountType  # Тип счета
    currency: str  # Валюта
    start_balance: Decimal  # Начальный остаток
    is_active: bool  # Признак активности
    text_color: str | None  # Цвет текста
    bg_color: str | None  # Цвет фона
    sort_position: int | None  # Позиция сортировки
    created_at: datetime  # Дата создания
    updated_at: datetime  # Дата обновления
    
    @classmethod
    def from_domain(cls, account):
        """Создать схему из доменной модели."""
        return cls(
            id=account.id,
            name=account.name,
            details=account.details,
            account_number=account.account_number,
            account_type=account.account_type,
            currency=account.currency,
            start_balance=account.start_balance,
            is_active=account.is_active,
            text_color=account.text_color,
            bg_color=account.bg_color,
            sort_position=account.sort_position,
            created_at=account.created_at,
            updated_at=account.updated_at
        )


class OperationalAccountListResponse(BaseModel):
    """Схема ответа со списком операционных счетов."""
    
    accounts: list[OperationalAccountResponse]  # Список счетов
    total: int  # Общее количество


class OperationalAccountBalanceResponse(BaseModel):
    """Схема ответа с балансом операционного счета на дату."""
    
    account_id: int  # ID счета
    account_name: str  # Название счета
    balance: Decimal  # Текущий баланс (вычисляется через транзакции)
    currency: str  # Валюта
    balance_date: date  # Дата расчета баланса


class OperationalAccountStatementRequest(BaseModel):
    """Схема запроса выписки по операционному счету."""
    
    account_id: int  # ID счета для выписки
    date_from: date  # Дата начала периода
    date_to: date  # Дата окончания периода
    format: str = Field(default="CSV", pattern="^(CSV|EXCEL|PDF)$")  # Формат экспорта


class OperationalAccountStatementResponse(BaseModel):
    """Схема ответа с выпиской по операционному счету."""
    
    account: OperationalAccountResponse  # Данные счета
    transactions: list['OperationalTransactionResponse']  # Транзакции за период
    opening_balance: Decimal  # Входящий остаток
    closing_balance: Decimal  # Исходящий остаток
    total_income: Decimal  # Сумма поступлений
    total_expense: Decimal  # Сумма списаний
    date_from: date  # Начало периода
    date_to: date  # Конец периода


class OperationalAccountReconciliationRequest(BaseModel):
    """Схема запроса сверки остатков по нескольким счетам."""
    
    account_ids: list[int]  # Список ID счетов для сверки
    date: date  # Дата сверки


class OperationalAccountReconciliationResponse(BaseModel):
    """Схема ответа со сверкой остатков."""
    
    reconciliation_date: date  # Дата сверки
    accounts: list[dict]  # Список счетов с балансами
    total_balance: Decimal  # Общий баланс по всем счетам
