# Настройка Alembic для Tomatoes ERP

## Конфигурация

### alembic.ini

- `sqlalchemy.url` закомментирован, URL берется из `app.config.settings`
- Путь к миграциям: `alembic/versions/`

### alembic/env.py

Настроен для:
- Автоматического импорта всех entities из `app/entities/`
- Использования `Base.metadata` из `app.core.database`
- Получения `DATABASE_URL` из `app.config.settings`

## Создание базы данных

### PostgreSQL

```bash
# Войти в PostgreSQL
psql -U postgres

# Выполнить скрипт
\i scripts/init_db.sql

# Или вручную:
CREATE DATABASE tomatoes_db;
CREATE USER tomatoes_user WITH PASSWORD 'tomatoes_pass';
GRANT ALL PRIVILEGES ON DATABASE tomatoes_db TO tomatoes_user;
```

### Переменные окружения

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=postgresql+asyncpg://tomatoes_user:tomatoes_pass@localhost:5432/tomatoes_db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Работа с миграциями

### Создание первой миграции

```bash
uv run alembic revision --autogenerate -m "initial migration"
```

Это создаст файл в `alembic/versions/` со всеми таблицами:

**Auth tables:**
- users
- roles
- permissions
- user_roles (many-to-many)
- role_permissions (many-to-many)

**Business tables:**
- products
- production_orders
- warehouses
- warehouse_items
- movements
- movement_items
- accounts
- transactions

### Применение миграций

```bash
# Применить все
uv run alembic upgrade head

# Применить следующую
uv run alembic upgrade +1

# Откатить последнюю
uv run alembic downgrade -1

# Откатить к конкретной версии
uv run alembic downgrade <revision>
```

### Просмотр информации

```bash
# Текущая версия БД
uv run alembic current

# История миграций
uv run alembic history --verbose

# Показать SQL без применения
uv run alembic upgrade head --sql
```

## Добавление новой Entity

1. Создайте файл entity в `app/entities/new_entity.py`
2. Добавьте импорт в `app/entities/__init__.py`
3. Добавьте импорт в `alembic/env.py` (в блок импорта entities)
4. Создайте миграцию:

```bash
uv run alembic revision --autogenerate -m "add new_entity table"
```

5. Проверьте сгенерированную миграцию в `alembic/versions/`
6. Примените миграцию:

```bash
uv run alembic upgrade head
```

## Особенности

### Async SQLAlchemy

- Используется `asyncpg` драйвер
- `DATABASE_URL` должен начинаться с `postgresql+asyncpg://`
- Alembic работает синхронно, но это нормально для миграций

### Soft Delete

Все entities наследуют поле `is_deleted` из `BaseEntity`, что позволяет использовать мягкое удаление.

### FastAPI-Users Integration

`UserEntity` интегрирован с FastAPI-Users через `SQLAlchemyBaseUserTable`, что добавляет стандартные поля для аутентификации.

## Troubleshooting

### Ошибка "relation already exists"

Если таблицы уже созданы вручную:

```bash
# Пометить текущее состояние как начальное
uv run alembic stamp head
```

### Ошибка импорта entities

Проверьте, что все entities импортированы в `alembic/env.py`.

### Ошибка подключения к БД

Проверьте:
1. PostgreSQL запущен
2. База данных создана
3. Пользователь имеет права
4. `DATABASE_URL` в `.env` корректен

