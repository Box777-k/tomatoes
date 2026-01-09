# Templates Documentation

Все Jinja2 шаблоны для web интерфейса с TailwindCSS.

## Структура

```
templates/
├── base.html                    # Базовый layout с sidebar навигацией
├── index.html                   # Dashboard
├── components/                  # Переиспользуемые компоненты
│   ├── table.html              # Таблицы с CRUD действиями
│   └── form.html               # Формы ввода данных
├── example_list.html           # Пример страницы списка
└── example_form.html           # Пример страницы формы
```

## base.html

Главный layout с:
- Вертикальной навигацией (sidebar) с Alpine.js
- Респонсивным дизайном (мобильный/desktop)
- TailwindCSS через CDN
- Навигацией по всем модулям (Production, Warehouse, Logistics, Finance)

### Блоки для переопределения

- `{% block title %}` - заголовок страницы
- `{% block content %}` - основной контент

## Компоненты

### table.html

Макрос `render_table()` для отображения списков с действиями:

```jinja
{% from "components/table.html" import render_table %}

{{ render_table(
    items=items,
    columns=[
        {'field': 'id', 'label': 'ID'},
        {'field': 'name', 'label': 'Name'},
    ],
    entity_name='order',
    entity_name_plural='orders',
    actions=True
) }}
```

### form.html

Макросы для форм:

```jinja
{% from "components/form.html" import render_form, render_field %}

{{ render_form(
    fields=[
        {'name': 'name', 'label': 'Name', 'type': 'text', 'required': True},
        {'name': 'description', 'label': 'Description', 'type': 'textarea'},
    ],
    action_url='/web/production/orders',
    submit_label='Save',
    cancel_url='/web/production/orders'
) }}
```

Поддерживаемые типы полей:
- `text` - текстовое поле
- `textarea` - многострочное поле
- `select` - выпадающий список
- `number` - числовое поле
- `date` - дата
- `email` - email

## Пример использования в контроллере

```python
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/orders")
async def list_orders(request: Request):
    items = []  # Получить из service
    return templates.TemplateResponse(
        "example_list.html",
        {
            "request": request,
            "items": items,
            "entity_name": "order",
            "entity_name_plural": "orders",
            "title": "Production Orders"
        }
    )
```

## Создание шаблонов для нового модуля

1. Создать папку `templates/{module_name}/`
2. Создать файлы:
   - `{plural}_list.html` - список (наследовать от base.html, использовать render_table)
   - `{singular}_detail.html` - детали
   - `{singular}_form.html` - форма (наследовать от base.html, использовать render_form)

Пример для production/orders:

```
templates/production/
├── orders_list.html
├── order_detail.html
└── order_form.html
```

## TailwindCSS

Используется через CDN в base.html. Все компоненты стилизованы с:
- Indigo цветовая схема для кнопок и навигации
- Респонсивные классы (sm:, lg:)
- Shadow и rounded классы для карточек

## Alpine.js

Используется для интерактивности sidebar (открытие/закрытие на мобильных).

