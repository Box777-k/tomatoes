# Соглашения по именованию (Naming Conventions)

## Разделение по уровням архитектуры

Согласно архитектуре контекстов система разделена на два уровня:
1. **Операционный уровень** (Operational) - оперативные операции
2. **Бухгалтерский уровень** (Accounting) - проводки, план счетов, закрытие периодов

## Правила именования

### 1. Entities (SQLAlchemy модели)

**Операционный уровень:**
- Префикс: `Operational`
- Суффикс: `Entity`
- Примеры:
  - `OperationalAccountEntity`
  - `OperationalTransactionEntity`
  - `OperationalCategoryEntity`

**Бухгалтерский уровень:**
- Префикс: `Accounting`
- Суффикс: `Entity`
- Примеры:
  - `AccountingAccountEntity` (план счетов)
  - `AccountingEntryEntity` (проводки)
  - `AccountingPeriodEntity` (периоды)

**Имена таблиц в БД:**
- Операционный: `operational_accounts`, `operational_transactions`
- Бухгалтерский: `accounting_accounts`, `accounting_entries`

### 2. Domain Models

**Операционный уровень:**
- Префикс: `Operational`
- Без суффикса
- Примеры:
  - `OperationalFinanceAccount`
  - `OperationalFinanceTransaction`
  - `OperationalTransactionCategory`

**Бухгалтерский уровень:**
- Префикс: `Accounting`
- Без суффикса
- Примеры:
  - `AccountingAccount`
  - `AccountingEntry`
  - `AccountingPeriod`

**Имена файлов:**
- Операционный: `operational_finance_account.py`, `operational_finance_transaction.py`
- Бухгалтерский: `accounting_account.py`, `accounting_entry.py`

### 3. Enums

**Операционный уровень:**
- Префикс: `Operational`
- Суффикс: `Type` или `Status`
- Примеры:
  - `OperationalAccountType`
  - `OperationalTransactionType`
  - `OperationalTransactionStatus`

**Бухгалтерский уровень:**
- Префикс: `Accounting`
- Суффикс: `Type` или `Status`
- Примеры:
  - `AccountingAccountType`
  - `AccountingEntryType`
  - `AccountingPeriodStatus`

**Имена файлов:**
- Операционный: `operational_account_enum.py`, `operational_transaction_enum.py`
- Бухгалтерский: `accounting_account_enum.py`, `accounting_entry_enum.py`

### 4. Pydantic Schemas

**Схемы ТРЕБУЮТ префикса контекста**, так как в одном модуле могут быть операционные и бухгалтерские сущности:

**Операционный уровень:**
- Префикс: `Operational`
- Примеры:
  - `OperationalAccountCreate`, `OperationalAccountUpdate`, `OperationalAccountResponse`
  - `OperationalTransactionCreate`, `OperationalTransactionResponse`

**Бухгалтерский уровень:**
- Префикс: `Accounting`
- Примеры:
  - `AccountingAccountCreate`, `AccountingAccountUpdate`, `AccountingAccountResponse`
  - `AccountingEntryCreate`, `AccountingEntryResponse`

**Расположение файлов:**
- Вариант 1: Все в одном файле `app/modules/finance/schemas.py` (с префиксами)
- Вариант 2: Разделить на `operational_schemas.py` и `accounting_schemas.py`

### 5. Repositories

**Префикс контекста обязателен:**
- Операционный: `OperationalAccountRepository`, `OperationalTransactionRepository`
- Бухгалтерский: `AccountingAccountRepository`, `AccountingEntryRepository`

**Имена файлов:**
- Операционный: `operational_account_repository.py`
- Бухгалтерский: `accounting_account_repository.py`

### 6. Services

**Префикс контекста обязателен:**
- Операционный: `OperationalAccountService`, `OperationalTransactionService`
- Бухгалтерский: `AccountingAccountService`, `AccountingEntryService`

**Имена файлов:**
- Операционный: `operational_account_service.py`
- Бухгалтерский: `accounting_account_service.py`

### 7. Mappers (Entity ↔ Domain)

**Имена классов:**
- `OperationalAccountMapper`
- `AccountingAccountMapper`

**Имена файлов:**
- `operational_account_mapper.py`
- `accounting_account_mapper.py`

## Структура модулей

**ВАЖНО**: Модули разделены по **предметным областям** (Finance, Logistics, Production, Warehouse), 
а НЕ по уровням архитектуры (Operational/Accounting).

В одном модуле могут находиться сущности ОБОИХ уровней архитектуры.

```
app/
├── entities/                        # SQLAlchemy модели
│   ├── operational_account.py       # OperationalAccountEntity
│   ├── operational_transaction.py   # OperationalTransactionEntity
│   ├── accounting_account.py        # AccountingAccountEntity
│   └── accounting_entry.py          # AccountingEntryEntity
│
├── enums/
│   ├── operational_account_enum.py      # OperationalAccountType
│   ├── operational_transaction_enum.py  # OperationalTransactionType
│   ├── accounting_account_enum.py       # AccountingAccountType
│   └── accounting_entry_enum.py         # AccountingEntryType
│
└── modules/
    ├── finance/                     # Модуль финансов (операционный + бухгалтерский)
    │   ├── models/
    │   │   ├── operational_finance_account.py
    │   │   ├── operational_finance_transaction.py
    │   │   ├── operational_transaction_category.py
    │   │   ├── accounting_account.py
    │   │   ├── accounting_entry.py
    │   │   └── accounting_period.py
    │   ├── repositories/
    │   │   ├── operational_account_repository.py
    │   │   ├── operational_transaction_repository.py
    │   │   ├── accounting_account_repository.py
    │   │   └── accounting_entry_repository.py
    │   ├── services/
    │   │   ├── operational_account_service.py
    │   │   ├── operational_transaction_service.py
    │   │   ├── accounting_account_service.py
    │   │   └── accounting_entry_service.py
    │   ├── mappers/
    │   │   ├── operational_account_mapper.py
    │   │   ├── operational_transaction_mapper.py
    │   │   ├── accounting_account_mapper.py
    │   │   └── accounting_entry_mapper.py
    │   └── schemas.py               # С ПРЕФИКСАМИ: OperationalAccount*, AccountingAccount*
    │
    ├── logistics/                   # Модуль логистики (операционный уровень)
    │   ├── models/
    │   ├── repositories/
    │   ├── services/
    │   └── schemas.py
    │
    ├── production/                  # Модуль производства (операционный уровень)
    │   ├── models/
    │   ├── repositories/
    │   ├── services/
    │   └── schemas.py
    │
    └── warehouse/                   # Модуль складской учет (операционный уровень)
        ├── models/
        ├── repositories/
        ├── services/
        └── schemas.py
```

## Исключения

### Общие сущности или системные (без префикса контекста)

Некоторые сущности используются на обоих уровнях и не требуют префикса:
- `UserEntity`, `RoleEntity`, `PermissionEntity` - аутентификация/авторизация
- `OrderEntity`, `ProductEntity` - бизнес-сущности верхнего уровня
- `WarehouseEntity`, `MovementEntity` - складской учет

### Справочники

Справочники могут быть:
- **Операционные** - используются только на операционном уровне (с префиксом `Operational`)
- **Бухгалтерские** - используются только в бухучете (с префиксом `Accounting`)
- **Общие** - используются на обоих уровнях (без префикса)

## Примеры полного именования

### Операционный счет (полный стек):

1. **Entity**: `OperationalAccountEntity` в `app/entities/operational_account.py`
2. **Domain Model**: `OperationalFinanceAccount` в `app/modules/finance/models/operational_finance_account.py`
3. **Enum**: `OperationalAccountType` в `app/enums/operational_account_enum.py`
4. **Schema**: `OperationalAccountCreate`, `OperationalAccountResponse` в `app/modules/finance/schemas.py`
5. **Repository**: `OperationalAccountRepository` в `app/modules/finance/repositories/operational_account_repository.py`
6. **Service**: `OperationalAccountService` в `app/modules/finance/services/operational_account_service.py`
7. **Mapper**: `OperationalAccountMapper` в `app/modules/finance/mappers/operational_account_mapper.py`

### Бухгалтерский счет (полный стек) - в том же модуле Finance:

1. **Entity**: `AccountingAccountEntity` в `app/entities/accounting_account.py`
2. **Domain Model**: `AccountingAccount` в `app/modules/finance/models/accounting_account.py`
3. **Enum**: `AccountingAccountType` в `app/enums/accounting_account_enum.py`
4. **Schema**: `AccountingAccountCreate`, `AccountingAccountResponse` в `app/modules/finance/schemas.py`
5. **Repository**: `AccountingAccountRepository` в `app/modules/finance/repositories/accounting_account_repository.py`
6. **Service**: `AccountingAccountService` в `app/modules/finance/services/accounting_account_service.py`
7. **Mapper**: `AccountingAccountMapper` в `app/modules/finance/mappers/accounting_account_mapper.py`

## Цель соглашений

1. **Четкое разделение контекстов** - сразу видно, к какому уровню относится сущность
2. **Избежание конфликтов имен** - нет путаницы между операционным и бухгалтерским счетом
3. **Улучшение читаемости** - код самодокументируется
4. **Упрощение поддержки** - легко находить нужные файлы и классы
