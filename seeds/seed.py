"""Seed script for initial data."""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.entities import OperationalAccountEntity, RoleEntity, PermissionEntity
from app.enums import OperationalAccountType


def seed_accounts(db: Session):
    """Seed operational accounts."""
    # Проверяем, есть ли уже данные
    if db.query(OperationalAccountEntity).count() > 0:
        print("Operational accounts already exist, skipping...")
        return
    
    accounts = [
        OperationalAccountEntity(
            name="Основной расчетный счет",
            account_number="40702810100000000001",
            account_type=OperationalAccountType.BANK,
            currency="RUB",
            start_balance=0,
            is_active=True
        ),
        OperationalAccountEntity(
            name="Касса организации",
            account_type=OperationalAccountType.CASH,
            currency="RUB",
            start_balance=0,
            is_active=True
        ),
    ]
    
    db.add_all(accounts)
    db.commit()
    print(f"Seeded {len(accounts)} accounts")


def seed_roles_permissions(db: Session):
    """Seed roles and permissions."""
    # Проверяем, есть ли уже данные
    if db.query(RoleEntity).count() > 0:
        print("Roles already exist, skipping...")
        return
    
    # Создаем разрешения
    permissions = [
        PermissionEntity(code="finance:accounts:read", description="Просмотр счетов"),
        PermissionEntity(code="finance:accounts:create", description="Создание счетов"),
        PermissionEntity(code="finance:accounts:update", description="Редактирование счетов"),
        PermissionEntity(code="finance:accounts:delete", description="Удаление счетов"),
    ]
    db.add_all(permissions)
    db.flush()
    
    # Создаем роли
    admin_role = RoleEntity(
        name="Администратор",
        description="Полный доступ к системе"
    )
    admin_role.permissions = permissions
    
    accountant_role = RoleEntity(
        name="Бухгалтер",
        description="Доступ к финансовым операциям"
    )
    accountant_role.permissions = [permissions[0], permissions[1], permissions[2]]
    
    db.add_all([admin_role, accountant_role])
    db.commit()
    print(f"Seeded {len(permissions)} permissions and 2 roles")


def main():
    """Run all seed functions."""
    print("Starting seeding...")
    
    db = SessionLocal()
    try:
        seed_accounts(db)
        seed_roles_permissions(db)
        print("Seeding completed successfully!")
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
