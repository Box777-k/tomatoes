"""Base controller with CRUD operations."""

from typing import Generic, TypeVar, Type, Any
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db

T = TypeVar('T')
templates = Jinja2Templates(directory="app/templates")


class BaseCRUDController(Generic[T]):
    """Base controller with CRUD operations for web interface."""
    
    def __init__(
        self,
        service_class: Type[Any],
        template_prefix: str,
        entity_name: str,
        entity_name_plural: str
    ):
        """
        Initialize base controller.
        
        Args:
            service_class: Service class for business logic
            template_prefix: Template path prefix (e.g., "production")
            entity_name: Entity name singular (e.g., "order")
            entity_name_plural: Entity name plural (e.g., "orders")
        """
        self.service_class = service_class
        self.template_prefix = template_prefix
        self.entity_name = entity_name
        self.entity_name_plural = entity_name_plural
    
    def get_service(self, db: AsyncSession = Depends(get_db)):
        """Get service instance."""
        return self.service_class(db)
    
    async def list_view(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ) -> HTMLResponse:
        """List all entities."""
        service = self.service_class(db)
        items = await service.get_all()
        
        return templates.TemplateResponse(
            f"{self.template_prefix}/{self.entity_name_plural}_list.html",
            {
                "request": request,
                "items": items,
                "entity_name": self.entity_name,
                "entity_name_plural": self.entity_name_plural,
                "title": f"{self.entity_name_plural.capitalize()}"
            }
        )
    
    async def detail_view(
        self,
        request: Request,
        item_id: int,
        db: AsyncSession = Depends(get_db)
    ) -> HTMLResponse:
        """Show entity detail."""
        service = self.service_class(db)
        item = await service.get_by_id(item_id)
        
        return templates.TemplateResponse(
            f"{self.template_prefix}/{self.entity_name}_detail.html",
            {
                "request": request,
                "item": item,
                "entity_name": self.entity_name,
                "title": f"{self.entity_name.capitalize()} Details"
            }
        )
    
    async def create_view(
        self,
        request: Request
    ) -> HTMLResponse:
        """Show create form."""
        return templates.TemplateResponse(
            f"{self.template_prefix}/{self.entity_name}_form.html",
            {
                "request": request,
                "entity_name": self.entity_name,
                "title": f"Create {self.entity_name.capitalize()}",
                "action": "create"
            }
        )
    
    async def edit_view(
        self,
        request: Request,
        item_id: int,
        db: AsyncSession = Depends(get_db)
    ) -> HTMLResponse:
        """Show edit form."""
        service = self.service_class(db)
        item = await service.get_by_id(item_id)
        
        return templates.TemplateResponse(
            f"{self.template_prefix}/{self.entity_name}_form.html",
            {
                "request": request,
                "item": item,
                "entity_name": self.entity_name,
                "title": f"Edit {self.entity_name.capitalize()}",
                "action": "edit"
            }
        )
    
    async def delete_action(
        self,
        item_id: int,
        db: AsyncSession = Depends(get_db)
    ) -> RedirectResponse:
        """Delete entity."""
        service = self.service_class(db)
        await service.delete(item_id)
        
        return RedirectResponse(
            url=f"/web/{self.template_prefix}/{self.entity_name_plural}",
            status_code=303
        )

