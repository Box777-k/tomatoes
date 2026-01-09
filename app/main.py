"""Main application entry point."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.middleware import setup_middleware
from app.core.events import startup_handler, shutdown_handler
from app.web.router import web_router

app = FastAPI(
    title="Tomatoes ERP",
    version="0.1.0",
    description="ERP system for production, warehouse, logistics and finance management"
)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup middleware
setup_middleware(app)

# Event handlers
app.add_event_handler("startup", startup_handler)
app.add_event_handler("shutdown", shutdown_handler)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}

# Mount web interface
app.include_router(web_router, prefix="/web")

# TODO: Add API routers when ready
# from app.api.v1.router import api_v1_router
# app.include_router(api_v1_router, prefix="/api/v1")

