"""Pydantic схемы для операционных категорий транзакций."""

from pydantic import BaseModel, Field
from datetime import datetime


class OperationalCategoryBase(BaseModel):
    """Базовая схема операционной категории (общие поля для Create/Update)."""
    
    name: str = Field(min_length=1, max_length=200)  # Название категории
    description: str | None = None  # Описание категории
    icon: str | None = Field(None, max_length=50)  # Иконка для UI
    color: str | None = Field(None, max_length=20)  # Основной цвет (hex)
    text_color: str | None = Field(None, max_length=20)  # Цвет текста (hex)
    bg_color: str | None = Field(None, max_length=20)  # Цвет фона (hex)
    sort_position: int | None = None  # Позиция при сортировке


class OperationalCategoryCreate(OperationalCategoryBase):
    """Схема для создания новой операционной категории."""
    
    parent_category_id: int | None = None  # ID родительской категории (None для корневых)


class OperationalCategoryUpdate(BaseModel):
    """Схема для обновления операционной категории (все поля опциональны)."""
    
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    icon: str | None = Field(None, max_length=50)
    color: str | None = Field(None, max_length=20)
    text_color: str | None = Field(None, max_length=20)
    bg_color: str | None = Field(None, max_length=20)
    sort_position: int | None = None
    parent_category_id: int | None = None  # Изменить родительскую категорию


class OperationalCategoryResponse(BaseModel):
    """Схема ответа с данными операционной категории."""
    
    id: int  # Идентификатор
    name: str  # Название
    description: str | None  # Описание
    icon: str | None  # Иконка
    color: str | None  # Основной цвет
    text_color: str | None  # Цвет текста
    bg_color: str | None  # Цвет фона
    sort_position: int | None  # Позиция сортировки
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
            color=category.color,
            text_color=category.text_color,
            bg_color=category.bg_color,
            sort_position=category.sort_position,
            is_system=category.is_system,
            created_at=category.created_at,
            updated_at=category.updated_at
        )


class OperationalCategoryTreeResponse(BaseModel):
    """Схема ответа с иерархическим деревом категорий.
    
    Рекурсивная структура для отображения вложенных категорий.
    """
    
    category: OperationalCategoryResponse  # Данные категории
    children: list['OperationalCategoryTreeResponse'] = []  # Дочерние категории


class OperationalCategoryListResponse(BaseModel):
    """Схема ответа со списком операционных категорий."""
    
    categories: list[OperationalCategoryResponse]  # Список категорий
    total: int  # Общее количество


# Включить forward references для рекурсивной модели
# Необходимо для работы вложенной структуры CategoryTreeResponse
OperationalCategoryTreeResponse.model_rebuild()
