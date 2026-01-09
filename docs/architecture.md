# Архитектура приложения Tomatoes

## Общая структура

Приложение построено на принципах Clean Architecture с четким разделением на слои и модули.

## Слои приложения

### 1. Enums (app/modules/*/enums/)

Статичные перечисления для бизнес-логики.

Назначение:
- Определяют допустимые значения и константы
- Изменяются только в коде приложения
- Используются в Entities, Models и Schemas для валидации
- Обеспечивают типобезопасность

Пример:
```python
from enum import Enum

class OperationalAccountType(str, Enum):
    BANK = "bank"
    CASH = "cash"
    WALLET = "wallet"
```

Важно: Enums не хранятся в БД как справочники, это hardcoded константы.

### 2. Entities (app/entities/)

SQLAlchemy модели, описывающие структуру таблиц в базе данных.

Назначение:
- Определяют схему БД (таблицы, колонки, типы данных)
- Содержат relationships между таблицами
- Наследуются от BaseEntity (id, created_at, updated_at, is_deleted)
- Соответствуют таблицам в БД 1:1

Пример:
```python
class OperationalAccountEntity(BaseEntity):
    __tablename__ = "operational_accounts"
    name = Column(String(200), nullable=False)
    account_type = Column(SQLEnum(OperationalAccountType), nullable=False)
    currency = Column(String(4), nullable=False, default="RUB")
    start_balance = Column(Numeric(12, 2), nullable=False, default=0)
```

Важно: Entities НЕ содержат бизнес-логику, только структуру данных.

### 3. Models (app/modules/*/models/)

Domain models - чистые Python dataclass с бизнес-логикой.

Назначение:
- Представляют бизнес-сущности без привязки к БД
- Содержат бизнес-логику и методы
- Независимы от фреймворков (SQLAlchemy, FastAPI)
- Могут иметь дополнительные поля для реализации логики
- Специфичны для каждого модуля

Пример:
```python
@dataclass
class OperationalFinanceAccount:
    id: int | None
    name: str
    account_type: OperationalAccountType
    currency: str
    is_active: bool
    
    def is_available_for_transaction(self) -> bool:
        return self.is_active and not self.is_deleted
```

Важно: Models содержат только бизнес-правила, не знают о БД и API.

### 4. Schemas (app/schemas/*/)

Pydantic модели для DTO (Data Transfer Objects)

Назначение:
- Валидация входящих данных из API
- Сериализация данных для отдачи в API
- Определение контрактов API endpoints
- Используются для валидации входящих данных и сериализации ответов

Типы схем:
- *Create - для создания записей (входящие данные)
- *Update - для обновления записей (входящие данные)
- *Response - для отдачи данных в API (исходящие данные)
- *List - для списков записей

Пример:
```python
class OperationalAccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    account_type: OperationalAccountType
    currency: str = Field(default="RUB")
    start_balance: Decimal = Field(default=0)

class OperationalAccountResponse(BaseModel):
    id: int
    name: str
    account_type: OperationalAccountType
    is_active: bool
```

Важно: Schemas не содержат бизнес-логики.

### 5. Mappers (app/modules/*/mappers.py)

Преобразователи между Entity и Model.

Назначение:
- Entity → Model (для загрузки из БД)
- Model → Entity (для сохранения в БД)
- Изолируют доменную логику от деталей БД

Пример:
```python
class OperationalFinanceAccountMapper:
    @staticmethod
    def to_domain(entity: OperationalAccountEntity) -> OperationalFinanceAccount:
        return OperationalFinanceAccount(
            id=entity.id,
            name=entity.name,
            account_type=entity.account_type,
            currency=entity.currency,
            is_active=entity.is_active
        )
    
    @staticmethod
    def to_entity(model: OperationalFinanceAccount) -> OperationalAccountEntity:
        return OperationalAccountEntity(
            id=model.id,
            name=model.name,
            account_type=model.account_type
        )
```

### 6. Repositories (app/modules/*/repositories.py)

Работа с базой данных.

Назначение:
- CRUD операции с entities
- Запросы к БД через SQLAlchemy
- Возвращают domain models (через mapper)
- Единственное место работы с БД

Пример:
```python
class OperationalFinanceAccountRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, account_id: int) -> OperationalFinanceAccount | None:
        entity = self.db.query(OperationalAccountEntity).filter(
            OperationalAccountEntity.id == account_id
        ).first()
        return OperationalFinanceAccountMapper.to_domain(entity) if entity else None
```

### 7. Services (app/modules/*/services.py)

Бизнес-логика приложения.

Назначение:
- Оркестрация между repositories
- Применение бизнес-правил
- Работа с domain models
- Транзакционная логика

Пример:
```python
class OperationalFinanceAccountService:
    def __init__(self, repository: OperationalFinanceAccountRepository):
        self.repository = repository
    
    def deactivate_account(self, account_id: int) -> OperationalFinanceAccount:
        account = self.repository.get_by_id(account_id)
        if not account.is_available_for_transaction():
            raise ValueError("Account not available")
        account.deactivate()
        return self.repository.update(account)
```

### 8. Controllers (app/web/controllers/)

Web-интерфейс (HTML шаблоны).

Назначение:
- Рендер HTML страниц
- Работа с Jinja2 templates
- Обработка форм

Наследуются от BaseCRUDController для стандартных операций.

## Поток данных

### API Request (FastAPI):
1. Request → Schema (валидация)
2. Schema → Service (бизнес-логика)
3. Service → Repository (работа с БД)
4. Repository → Mapper → Entity (SQLAlchemy)
5. Entity → Mapper → Model (domain)
6. Model → Service → Schema (Response)
7. Schema → Response (JSON)

### Web Request (HTML):
1. Request → Controller
2. Controller → Service
3. Service → Repository → Model
4. Model → Controller → Template
5. Template → Response (HTML)

## Модульная структура

Каждый модуль (users, finance, warehouse, logistics, production) содержит:

```
module/
├── __init__.py
├── enums/             # Перечисления и константы
├── models/            # Domain models
├── schemas/           # Pydantic schemas (опционально, если специфичны для модуля)
├── mappers.py         # Entity ↔ Model
├── repositories.py    # БД операции
├── services.py        # Бизнес-логика
└── dependencies.py    # FastAPI dependencies
```

Примечание: Schemas общие для модулей находятся в app/schemas/{module}/

## Принципы

1. Enums - статичные константы в коде, не справочники в БД
2. Entities - только структура БД, без логики
3. Models - бизнес-логика, независимая от БД и API
4. Schemas - контракты API, валидация данных
5. Mappers - изолируют БД от бизнес-логики
6. Repositories - единственное место работы с БД
7. Services - оркестрация, применение бизнес-правил
8. Controllers работают только со Schemas
9. Каждый слой зависит только от слоев ниже

## Зависимости между слоями

```
Controllers/API Endpoints
        ↓
     Schemas (валидация/сериализация)
        ↓
     Services
        ↓
   Repositories
        ↓
     Mappers
     ↓     ↓
  Models  Entities
     ↓     ↓
      Enums
```

- Schemas используются на границе (API endpoints) для преобразования в/из Models
- Enums используются во всех слоях для типобезопасности
- Каждый слой зависит только от слоев ниже себя
