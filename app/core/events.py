"""Application startup and shutdown event handlers."""

import logging

logger = logging.getLogger(__name__)


async def startup_handler() -> None:
    """Handle application startup."""
    logger.info("Starting Tomatoes ERP application...")
    # TODO: Initialize database connections, load configuration, etc.


async def shutdown_handler() -> None:
    """Handle application shutdown."""
    logger.info("Shutting down Tomatoes ERP application...")
    # TODO: Close database connections, cleanup resources, etc.

