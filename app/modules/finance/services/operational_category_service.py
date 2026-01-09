"""Operational transaction category service."""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from ..repositories import (
    OperationalTransactionCategoryRepository,
    OperationalTransactionCategoryTreeRepository,
)
from ..models import OperationalTransactionCategory
from ...entities import OperationalTransactionEntity


class OperationalTransactionCategoryService:
    """Service for operational transaction category business logic."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.category_repo = OperationalTransactionCategoryRepository(session)
        self.tree_repo = OperationalTransactionCategoryTreeRepository(session)
    
    async def create_category(
        self,
        category: OperationalTransactionCategory,
        parent_id: Optional[int] = None
    ) -> OperationalTransactionCategory:
        """Create new category.
        
        Business rules:
        - System categories can only be created programmatically
        - Parent category must exist and be active if provided
        """
        # Validate parent if provided
        if parent_id:
            parent = await self.category_repo.get_by_id(parent_id)
            if not parent:
                raise ValueError(f"Parent category with id {parent_id} not found")
            
            if not parent.is_active:
                raise ValueError("Parent category must be active")
        
        return await self.category_repo.create(category, parent_id)
    
    async def update_category(
        self,
        category: OperationalTransactionCategory
    ) -> OperationalTransactionCategory:
        """Update existing category.
        
        Business rules:
        - Cannot change is_system flag
        - Cannot update system categories
        """
        existing = await self.category_repo.get_by_id(category.id)
        if not existing:
            raise ValueError(f"Category with id {category.id} not found")
        
        if existing.is_system:
            raise ValueError("System categories cannot be updated")
        
        return await self.category_repo.update(category)
    
    async def delete_category(self, category_id: int) -> bool:
        """Delete category.
        
        Business rules:
        - Cannot delete system categories
        - Cannot delete if category has transactions
        - Cannot delete if category has children
        """
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            raise ValueError(f"Category with id {category_id} not found")
        
        if category.is_system:
            raise ValueError("System categories cannot be deleted")
        
        # Check if category has transactions
        has_transactions = await self._category_has_transactions(category_id)
        if has_transactions:
            raise ValueError("Cannot delete category with existing transactions")
        
        # Check if category has children
        children_ids = await self.tree_repo.get_children_ids(category_id)
        if children_ids:
            raise ValueError("Cannot delete category with children. Delete children first.")
        
        return await self.category_repo.delete(category_id)
    
    async def get_category_tree(self) -> list[dict]:
        """Get hierarchical category tree.
        
        Returns tree structure with nested children.
        """
        # Get all categories
        all_categories = await self.category_repo.get_all(include_inactive=False)
        
        # Get root categories
        root_ids = await self.tree_repo.get_root_category_ids()
        
        # Build tree recursively
        tree = []
        for root_id in root_ids:
            root_cat = next((c for c in all_categories if c.id == root_id), None)
            if root_cat:
                tree_node = await self._build_tree_node(root_cat, all_categories)
                tree.append(tree_node)
        
        return tree
    
    async def get_system_transfer_category(self) -> Optional[OperationalTransactionCategory]:
        """Get system transfer category.
        
        This category is used for transfers between accounts.
        """
        all_categories = await self.category_repo.get_all(include_inactive=True)
        
        # Find category with is_system=True and name containing "Перемещение"
        for category in all_categories:
            if category.is_system and "Перемещение" in category.name:
                return category
        
        return None
    
    async def get_category_path(self, category_id: int) -> list[OperationalTransactionCategory]:
        """Get full path from root to category."""
        path_ids = await self.tree_repo.get_path(category_id)
        
        categories = []
        for cat_id in path_ids:
            category = await self.category_repo.get_by_id(cat_id)
            if category:
                categories.append(category)
        
        return categories
    
    async def move_category(
        self,
        category_id: int,
        new_parent_id: Optional[int]
    ) -> OperationalTransactionCategory:
        """Move category to new parent.
        
        Business rules:
        - Cannot move system categories
        - Cannot move to own descendant (circular reference)
        - New parent must be active if provided
        """
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            raise ValueError(f"Category with id {category_id} not found")
        
        if category.is_system:
            raise ValueError("System categories cannot be moved")
        
        # Validate new parent
        if new_parent_id:
            new_parent = await self.category_repo.get_by_id(new_parent_id)
            if not new_parent:
                raise ValueError(f"New parent category with id {new_parent_id} not found")
            
            if not new_parent.is_active:
                raise ValueError("New parent category must be active")
            
            # Check for circular reference
            descendants = await self.tree_repo.get_descendants(category_id)
            descendant_ids = [desc_id for desc_id, _ in descendants]
            if new_parent_id in descendant_ids:
                raise ValueError("Cannot move category to its own descendant")
        
        # Move in tree
        await self.tree_repo.move_category(category_id, new_parent_id)
        
        # Return updated category
        return await self.category_repo.get_by_id(category_id)
    
    async def _build_tree_node(
        self,
        category: OperationalTransactionCategory,
        all_categories: list[OperationalTransactionCategory]
    ) -> dict:
        """Build tree node recursively."""
        # Get children of this category
        children_ids = await self.tree_repo.get_children_ids(category.id)
        
        children = []
        for child_id in children_ids:
            child_cat = next((c for c in all_categories if c.id == child_id), None)
            if child_cat:
                child_node = await self._build_tree_node(child_cat, all_categories)
                children.append(child_node)
        
        return {
            "category": category,
            "children": children
        }
    
    async def _category_has_transactions(self, category_id: int) -> bool:
        """Check if category has any transactions."""
        stmt = select(OperationalTransactionEntity).where(
            and_(
                OperationalTransactionEntity.category_id == category_id,
                OperationalTransactionEntity.is_deleted == False
            )
        ).limit(1)
        
        result = await self.session.execute(stmt)
        return result.first() is not None
