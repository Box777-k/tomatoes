"""Users web controller."""

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.modules.users.services import UserService
from app.modules.users.repositories import UserRepository

router = APIRouter(tags=["users-web"])
templates = Jinja2Templates(directory="app/templates")


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """Get user service."""
    return UserService(UserRepository(db))


@router.get("/users", response_class=HTMLResponse)
async def list_users(
    request: Request,
    service: UserService = Depends(get_user_service)
):
    """List all users."""
    users = await service.get_all_users()
    
    return templates.TemplateResponse(
        "users/users_list.html",
        {
            "request": request,
            "users": users,
            "title": "Users"
        }
    )


@router.get("/users/create", response_class=HTMLResponse)
async def create_user_form(request: Request):
    """Show create user form."""
    return templates.TemplateResponse(
        "users/user_form.html",
        {
            "request": request,
            "title": "Create User",
            "action": "create",
            "user": None
        }
    )


@router.post("/users/create")
async def create_user(
    email: str = Form(...),
    password: str = Form(...),
    first_name: str = Form(None),
    last_name: str = Form(None),
    phone: str = Form(None),
    is_superuser: bool = Form(False),
    service: UserService = Depends(get_user_service)
):
    """Create new user."""
    try:
        user = await service.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            is_superuser=is_superuser
        )
        return RedirectResponse(url="/web/users", status_code=303)
    except Exception as e:
        # TODO: Show error in form
        return RedirectResponse(url="/web/users/create", status_code=303)


@router.get("/users/{user_id}", response_class=HTMLResponse)
async def user_detail(
    request: Request,
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Show user details."""
    user = await service.get_user(user_id)
    
    return templates.TemplateResponse(
        "users/user_detail.html",
        {
            "request": request,
            "user": user,
            "title": f"User: {user.email}"
        }
    )


@router.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def edit_user_form(
    request: Request,
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Show edit user form."""
    user = await service.get_user(user_id)
    
    return templates.TemplateResponse(
        "users/user_form.html",
        {
            "request": request,
            "title": "Edit User",
            "action": "edit",
            "user": user
        }
    )


@router.post("/users/{user_id}/edit")
async def update_user(
    user_id: int,
    email: str = Form(...),
    first_name: str = Form(None),
    last_name: str = Form(None),
    phone: str = Form(None),
    service: UserService = Depends(get_user_service)
):
    """Update user."""
    try:
        await service.update_user(
            user_id=user_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        return RedirectResponse(url=f"/web/users/{user_id}", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/web/users/{user_id}/edit", status_code=303)


@router.post("/users/{user_id}/delete")
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Delete user."""
    await service.delete_user(user_id)
    return RedirectResponse(url="/web/users", status_code=303)


@router.post("/users/{user_id}/activate")
async def activate_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Activate user."""
    await service.activate_user(user_id)
    return RedirectResponse(url=f"/web/users/{user_id}", status_code=303)


@router.post("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Deactivate user."""
    await service.deactivate_user(user_id)
    return RedirectResponse(url=f"/web/users/{user_id}", status_code=303)

