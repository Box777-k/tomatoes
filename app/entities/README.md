# Database Entities

Все SQLAlchemy entities (таблицы БД) находятся в этой папке.

## Структура

### Auth Entities (Аутентификация и авторизация)

- **user.py** - Пользователи (UserEntity) с интеграцией FastAPI-Users
- **role.py** - Роли (RoleEntity) для RBAC
- **permission.py** - Разрешения (PermissionEntity) 
- **user_role.py** - Связь many-to-many между пользователями и ролями
- **role_permission.py** - Связь many-to-many между ролями и разрешениями

### Business Entities (Бизнес-домен)

#### Production (Производство)
- **product.py** - Продукты
- **production_order.py** - Производственные заказы

#### Warehouse (Склад)
- **warehouse.py** - Склады
- **warehouse_item.py** - Остатки на складах

#### Logistics (Логистика)
- **movement.py** - Перемещения между складами
- **movement_item.py** - Позиции в перемещениях

#### Finance (Финансы)
- **account.py** - Счета
- **transaction.py** - Финансовые транзакции

## Базовый класс

**base.py** - BaseEntity содержит общие поля:
- id
- created_at
- updated_at
- is_deleted (soft delete)

## RBAC модель

```
User (many) ←→ (many) Role (many) ←→ (many) Permission
```

Пример разрешений:
- `production:orders:create` - создание производственных заказов
- `warehouse:items:read` - просмотр остатков на складе
- `finance:transactions:delete` - удаление транзакций

## Использование в модулях

Модули импортируют entities через центральный `__init__.py`:

```python
from app.entities import OrderEntity, ProductEntity
```

Mappers в модулях преобразуют entities в domain models и обратно.

