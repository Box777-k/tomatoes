"""Seed script for initial data."""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.entities import OperationalAccountEntity, OperationalCategoryEntity, RoleEntity, PermissionEntity
from app.modules.finance.enums import OperationalAccountType


def seed_operational_accounts(db: Session):
    """Seed operational finance accounts."""
    # Проверяем, есть ли уже данные
    if db.query(OperationalAccountEntity).count() > 0:
        print("Operational accounts already exist, skipping...")
        return
    
    accounts = [
        OperationalAccountEntity(
            name="Основной",
            details="Основной корпоративный счет",
            account_number="40702810100000000001",
            account_type=OperationalAccountType.NON_CASH,
            currency="RUB",
            start_balance=0,
            is_active=True,
            text_color="#1e3a8a",
            bg_color="#dbeafe",
            sort_position=1
        ),
        OperationalAccountEntity(
            name="Инвестиционный",
            details="Инвестиционный счет Николай",
            account_number="40702810100000000002",
            account_type=OperationalAccountType.NON_CASH,
            currency="RUB",
            start_balance=0,
            is_active=True,
            text_color="#1e3a8a",
            bg_color="#e0e7ff",
            sort_position=2
        ),
        OperationalAccountEntity(
            name="Главная касса",
            details="Наличные денежные средства",
            account_type=OperationalAccountType.CASH,
            currency="RUB",
            start_balance=0,
            is_active=True,
            text_color="#166534",
            bg_color="#dcfce7",
            sort_position=3
        ),
    ]
    
    db.add_all(accounts)
    db.commit()
    print(f"Seeded {len(accounts)} operational accounts")


def seed_operational_categories(db: Session):
    """Seed operational transaction categories."""
    # Проверяем, есть ли уже данные
    if db.query(OperationalCategoryEntity).count() > 0:
        print("Operational categories already exist, skipping...")
        return
    
    categories = [
        # Системная категория для переводов между счетами
        OperationalCategoryEntity(
            name="Перемещение между счетами",
            description="Системная категория для операций перевода денег между счетами организации",
            icon="transfer",
            text_color="#6b7280",
            bg_color="#f3f4f6",
            sort_position=1,
            is_active=True,
            is_system=True
        ),
        
        # Категории доходов
        OperationalCategoryEntity(
            name="Поступления от продаж",
            description="Доходы от реализации продукции и услуг",
            icon="cash-register",
            text_color="#065f46",
            bg_color="#d1fae5",
            sort_position=10,
            is_active=True,
            is_system=False
        ),
        OperationalCategoryEntity(
            name="Прочие доходы",
            description="Прочие поступления денежных средств",
            icon="plus-circle",
            text_color="#047857",
            bg_color="#d1fae5",
            sort_position=20,
            is_active=True,
            is_system=False
        ),
        
        # Категории расходов
        OperationalCategoryEntity(
            name="Зарплата и налоги",
            description="Выплаты заработной платы и налогов с ФОТ",
            icon="users",
            text_color="#991b1b",
            bg_color="#fee2e2",
            sort_position=100,
            is_active=True,
            is_system=False
        ),
        OperationalCategoryEntity(
            name="Закупка материалов",
            description="Расходы на приобретение сырья и материалов",
            icon="shopping-cart",
            text_color="#b91c1c",
            bg_color="#fecaca",
            sort_position=110,
            is_active=True,
            is_system=False
        ),
        OperationalCategoryEntity(
            name="Операционные расходы",
            description="Аренда, коммунальные услуги, офисные расходы",
            icon="building",
            text_color="#dc2626",
            bg_color="#fecaca",
            sort_position=120,
            is_active=True,
            is_system=False
        ),
    ]
    
    db.add_all(categories)
    db.commit()
    print(f"Seeded {len(categories)} operational categories")


def seed_roles_permissions(db: Session):
    """Seed roles and permissions."""
    # Проверяем, есть ли уже данные
    if db.query(RoleEntity).count() > 0:
        print("Roles already exist, skipping...")
        return
    
    # Создаем разрешения для финансов
    permissions = [
        PermissionEntity(
            name="Просмотр счетов",
            code="finance:accounts:read",
            resource="finance",
            action="read",
            description="Просмотр операционных счетов"
        ),
        PermissionEntity(
            name="Создание счетов",
            code="finance:accounts:create",
            resource="finance",
            action="create",
            description="Создание операционных счетов"
        ),
        PermissionEntity(
            name="Редактирование счетов",
            code="finance:accounts:update",
            resource="finance",
            action="update",
            description="Редактирование операционных счетов"
        ),
        PermissionEntity(
            name="Удаление счетов",
            code="finance:accounts:delete",
            resource="finance",
            action="delete",
            description="Удаление операционных счетов"
        ),
        PermissionEntity(
            name="Просмотр транзакций",
            code="finance:transactions:read",
            resource="finance",
            action="read",
            description="Просмотр финансовых операций"
        ),
        PermissionEntity(
            name="Создание транзакций",
            code="finance:transactions:create",
            resource="finance",
            action="create",
            description="Создание финансовых операций"
        ),
    ]
    db.add_all(permissions)
    db.flush()
    
    # Создаем роли
    admin_role = RoleEntity(
        name="Администратор",
        code="admin",
        description="Полный доступ к системе"
    )
    admin_role.permissions = permissions
    
    accountant_role = RoleEntity(
        name="Бухгалтер",
        code="accountant",
        description="Доступ к финансовым операциям"
    )
    accountant_role.permissions = permissions  # Все финансовые права
    
    db.add_all([admin_role, accountant_role])
    db.commit()
    print(f"Seeded {len(permissions)} permissions and 2 roles")


def main():
    """Run all seed functions."""
    print("Starting seeding...")
    
    db = SessionLocal()
    try:
        seed_operational_accounts(db)
        seed_operational_categories(db)
        seed_roles_permissions(db)
        print("Seeding completed successfully!")
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
