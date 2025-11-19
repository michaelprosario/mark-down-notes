"""Error handling middleware for FastAPI."""

import logging
from typing import Callable
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import traceback

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:
    """
    Middleware for centralized error handling.
    
    Catches exceptions and returns consistent error responses.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                # You can modify headers here if needed
                pass
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as exc:
            # Handle the exception
            response = await self._handle_exception(exc)
            await response(scope, receive, send)

    async def _handle_exception(self, exc: Exception) -> JSONResponse:
        """
        Handle different types of exceptions.
        
        Args:
            exc: The exception to handle.
        
        Returns:
            JSONResponse with appropriate error message and status code.
        """
        # Database errors
        if isinstance(exc, IntegrityError):
            logger.error(f"Database integrity error: {exc}")
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "error": "Database constraint violation",
                    "message": "The operation violates a database constraint (duplicate key, foreign key, etc.)",
                    "detail": str(exc.orig) if hasattr(exc, 'orig') else str(exc),
                },
            )

        if isinstance(exc, SQLAlchemyError):
            logger.error(f"Database error: {exc}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Database error",
                    "message": "An error occurred while accessing the database",
                },
            )

        # Validation errors (from Pydantic)
        if hasattr(exc, 'errors'):
            logger.warning(f"Validation error: {exc}")
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "error": "Validation error",
                    "message": "Request validation failed",
                    "errors": exc.errors(),
                },
            )

        # Generic server errors
        logger.exception(f"Unhandled exception: {exc}")
        logger.error(traceback.format_exc())
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred",
                "detail": str(exc) if logger.level == logging.DEBUG else None,
            },
        )


async def error_handler_middleware(request: Request, call_next: Callable) -> Response:
    """
    Alternative middleware function format for error handling.
    
    Args:
        request: The incoming request.
        call_next: The next middleware or route handler.
    
    Returns:
        Response from the handler or error response.
    """
    try:
        response = await call_next(request)
        return response
    except IntegrityError as exc:
        logger.error(f"Database integrity error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "Database constraint violation",
                "message": "The operation violates a database constraint",
                "detail": str(exc.orig) if hasattr(exc, 'orig') else str(exc),
            },
        )
    except SQLAlchemyError as exc:
        logger.error(f"Database error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Database error",
                "message": "An error occurred while accessing the database",
            },
        )
    except Exception as exc:
        logger.exception(f"Unhandled exception: {exc}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred",
            },
        )
