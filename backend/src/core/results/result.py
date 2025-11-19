"""Result wrapper for service operations."""

from typing import Generic, TypeVar, Optional, List
from dataclasses import dataclass

T = TypeVar('T')


@dataclass
class Result(Generic[T]):
    """Result wrapper for success/failure handling."""

    is_success: bool
    value: Optional[T] = None
    error: Optional[str] = None
    message: Optional[str] = None
    validation_errors: Optional[List[str]] = None

    @staticmethod
    def success(value: T, message: str = "") -> 'Result[T]':
        """Create a successful result."""
        return Result(
            is_success=True,
            value=value,
            message=message,
        )

    @staticmethod
    def failure(error: str, validation_errors: Optional[List[str]] = None) -> 'Result[T]':
        """Create a failed result."""
        return Result(
            is_success=False,
            error=error,
            validation_errors=validation_errors or [],
        )

    def __bool__(self) -> bool:
        """Allow Result to be used in boolean context."""
        return self.is_success
