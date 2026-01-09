"""Production order entity."""

from sqlalchemy import Column, Integer, String, ForeignKey
from .base import BaseEntity


class OrderEntity(BaseEntity):
    """Production order table."""
    
    __tablename__ = "orders"
    __table_args__ = {'comment': 'Заказы клиентов'}
    
    order_number = Column(String(50), unique=True, nullable=False, index=True, comment="Номер заказа на производство")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="Идентификатор производимой номенклатуры")
    quantity = Column(Integer, nullable=False, comment="Количество к производству")
    status = Column(String(20), nullable=False, index=True, comment="Статус заказа (системный список)")

