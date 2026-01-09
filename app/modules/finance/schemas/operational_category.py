"""Pydantic схемы для операционных категорий транзакций."""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class OperationalTransactionCategoryBase(BaseModel):
    """Базовая схема операционной категории (общие поля для Create/Update)."""
    
    name: str = Field(min_length=1, max_length=200)  # Название категории
    description: str | None = None  # Описание категории
    icon: str | None = Field(None, max_length=50)  # Иконка для UI
    text_color: str | None = Field(None, max_length=7)  # Цвет текста (hex)
    bg_color: str | None = Field(None, max_length=7)  # Цвет фона (hex)
    sort_position: int | None = None  # Позиция при сортировке


class OperationalTransactionCategoryCreate(OperationalTransactionCategoryBase):
    """Схема для создания новой операционной категории.
    
    Поддерживает иерархическую структуру через parent_id.
    """
    
    parent_id: int | None = None  # ID родительской категории (None для корневых)


class OperationalTransactionCategoryUpdate(BaseModel):
    """Схема для обновления операционной категории (все поля опциональны).
    
    Примечание: изменение is_system не допускается через API.
    """
    
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    icon: str | None = Field(None, max_length=50)
    text_color: str | None = Field(None, max_length=7)
    bg_color: str | None = Field(None, max_length=7)
    sort_position: int | None = None
    parent_id: int | None = None  # Изменить родительскую категорию
    
    @field_validator('parent_id')
    @classmethod
    def validate_parent_not_self(cls, v):
        """Проверка что категория не может быть родителем самой себя (будет проверено в сервисе)."""
        return v


class OperationalTransactionCategoryResponse(BaseModel):
    """Схема ответа с данными операционной категории."""
    
    id: int  # Идентификатор
    name: str  # Название
    description: str | None  # Описание
    icon: str | None  # Иконка
    text_color: str | None  # Цвет текста
    bg_color: str | None  # Цвет фона
    sort_position: int | None  # Позиция сортировки
    is_active: bool  # Признак активности
    is_system: bool  # Признак системной категории (не удаляемая пользователем)
    created_at: datetime  # Дата создания
    updated_at: datetime  # Дата обновления
    
    @classmethod
    def from_domain(cls, category):
        """Создать схему из доменной модели."""
        return cls(
            id=category.id,
            name=category.name,
            description=category.description,
            icon=category.icon,
            text_color=category.text_color,
            bg_color=category.bg_color,
            sort_position=category.sort_position,
            is_active=category.is_active,
            is_system=category.is_system,
            created_at=category.created_at,
            updated_at=category.updated_at
        )


class OperationalTransactionCategoryWithPathResponse(OperationalTransactionCategoryResponse):
    """Схема ответа с данными категории и полным путем в дереве."""
    
    full_path: str  # Полный путь категории в дереве (например, "Расходы / Зарплата / Налоги")
    level: int  # Уровень вложенности (0 для корневых)


class OperationalTransactionCategoryTreeNode(BaseModel):
    """Узел дерева категорий (рекурсивная структура)."""
    
    category: OperationalTransactionCategoryResponse  # Данные категории
    children: list['OperationalTransactionCategoryTreeNode'] = []  # Дочерние категории


class OperationalTransactionCategoryTreeResponse(BaseModel):
    """Схема ответа с иерархическим деревом категорий."""
    
    tree: list[OperationalTransactionCategoryTreeNode]  # Корневые категории с детьми
    total: int  # Общее количество категорий


class OperationalTransactionCategoryListResponse(BaseModel):
    """Схема ответа со списком операционных категорий (плоский список)."""
    
    categories: list[OperationalTransactionCategoryResponse]  # Список категорий
    total: int  # Общее количество


# Включить forward references для рекурсивной модели
# Необходимо для работы вложенной структуры CategoryTreeNode
OperationalTransactionCategoryTreeNode.model_rebuild()
