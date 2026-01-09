"""Main web router for SSR."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .controllers.users import router as users_router

web_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@web_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Dashboard page."""
    return templates.TemplateResponse("index.html", {"request": request})


# Include controllers
web_router.include_router(users_router)

# TODO: Include more controllers when ready
# from .controllers.production import router as production_web_router
# web_router.include_router(production_web_router, prefix="/production")
