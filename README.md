# Tomatoes ERP

ERP система для управления производством, складом, логистикой и финансами.

## Архитектура

Проект построен на основе DDD (Domain-Driven Design) с четкой слоистой архитектурой:

### Структура проекта

```
tomatoes/
├── app/
│   ├── api/                 # REST API слой (пусто, для будущей разработки)
│   ├── web/                 # Web Controllers для SSR (пусто)
│   ├── core/                # Ядро приложения
│   ├── entities/            # SQLAlchemy entities (БД таблицы)
│   ├── modules/             # Бизнес-модули
│   │   ├── production/      # Модуль производства
│   │   ├── warehouse/       # Модуль складирования
│   │   ├── logistics/       # Модуль логистики
│   │   └── finance/         # Модуль финансов
│   ├── templates/           # Jinja2 шаблоны
│   └── static/              # Статические файлы
├── alembic/                 # Миграции БД
└── tests/                   # Тесты
```

### Слои приложения

**Entities (app/entities/)** - SQLAlchemy модели БД, централизованное хранение всех таблиц

**Модули (app/modules/)** - каждый модуль содержит:
- **models.py** - Domain models с бизнес-логикой
- **mappers.py** - Преобразование entities ↔ domain models
- **repositories.py** - Доступ к данным
- **services.py** - Бизнес-логика модуля
- **schemas.py** - Pydantic схемы для валидации

### Клиенты

Система поддерживает три типа клиентов:
1. Desktop Web App (SSR через Jinja2)
2. Mobile Web App (REST API)
3. Telegram Bot (REST API)

## Установка

```bash
# Установка зависимостей
uv sync

# Создание .env файла (или создайте вручную)
# DATABASE_URL=postgresql+asyncpg://tomatoes_user:tomatoes_pass@localhost:5432/tomatoes_db

# Создание базы данных PostgreSQL
psql -U postgres -f scripts/init_db.sql

# Применение миграций
uv run alembic upgrade head

# Запуск приложения
uv run uvicorn app.main:app --reload
```

Приложение будет доступно:
- Web интерфейс: http://localhost:8000/web
- API: http://localhost:8000/api/v1
- Docs: http://localhost:8000/docs

## Разработка

### Миграции БД

```bash
# Создание новой миграции
uv run alembic revision --autogenerate -m "add new table"

# Применение всех миграций
uv run alembic upgrade head

# Откат одной миграции
uv run alembic downgrade -1

# Просмотр текущей версии
uv run alembic current

# История миграций
uv run alembic history
```

### Тестирование

```bash
# Запуск тестов
pytest
```

### Скрипты

```bash
# Создание миграции (bash)
./scripts/create_migration.sh "description"

# Применение миграций (bash)
./scripts/apply_migrations.sh
```

## Web интерфейс

Web интерфейс доступен по адресу `http://localhost:8000/web`

### Базовый контроллер

Используйте `BaseCRUDController` для быстрого создания CRUD интерфейса:

```python
from app.common.base_controller import BaseCRUDController

class MyController(BaseCRUDController):
    def __init__(self):
        super().__init__(
            service_class=MyService,
            template_prefix="my_module",
            entity_name="item",
            entity_name_plural="items"
        )
```

### Шаблоны

- Все шаблоны с TailwindCSS
- Вертикальная навигация (sidebar)
- Компоненты для таблиц и форм
- Полная документация в `app/templates/README.md`

## Технологии

- FastAPI - веб-фреймворк
- SQLAlchemy - ORM
- Alembic - миграции БД
- Pydantic - валидация данных
- Jinja2 - SSR шаблоны
- FastAPI-Users - управление пользователями и аутентификация
- Casbin - RBAC авторизация
- PostgreSQL - база данных

