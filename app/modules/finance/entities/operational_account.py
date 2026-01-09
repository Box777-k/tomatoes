"""Operational account entity."""

from sqlalchemy import Column, String, Numeric, Boolean, Integer, Enum as SQLEnum
from app.modules.finance.enums import OperationalAccountType
from app.entities.base import BaseEntity


class OperationalAccountEntity(BaseEntity):
    """Operational account table."""
    
    __tablename__ = "operational_accounts"
    __table_args__ = {'comment': 'Операционные счета организации'}
    
    name = Column(String(200), nullable=False, comment="Наименование счета")
    details = Column(String, nullable=True, comment="Дополнительная информация о счете")
    account_number = Column(String(100), unique=True, nullable=True, index=True, comment="Номер счета")
    account_type = Column(SQLEnum(OperationalAccountType), nullable=False, comment="Тип счета (наличный/безналичный)")
    currency = Column(String(4), nullable=False, default="RUB", comment="Валюта счета (код ISO 4217)")
    start_balance = Column(Numeric(12, 2), nullable=False, default=0, comment="Начальный остаток на счете")
    is_active = Column(Boolean, nullable=False, default=True, comment="Признак активности счета")
    text_color = Column(String(7), nullable=True, comment="Цвет текста для визуального отображения (HEX)")
    bg_color = Column(String(7), nullable=True, comment="Цвет фона для визуального отображения (HEX)")
    sort_position = Column(Integer, nullable=True, default=0, comment="Позиция сортировки")