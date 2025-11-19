"""Result object for service operations following Clean Architecture."""

from typing import Generic, TypeVar, Optional, List
from dataclasses import dataclass, field

T = TypeVar('T')


@dataclass
class ValidationError:
    """Represents a validation error."""
    field: str
    message: str


@dataclass
class Result(Generic[T]):
    """
    Generic result object for service operations.
    
    Encapsulates success/failure state with data, messages, and validation errors.
    Avoids throwing exceptions for expected business failures.
    """
    success: bool
    data: Optional[T] = None
    message: str = ""
    errors: List[ValidationError] = field(default_factory=list)
    
    @staticmethod
    def ok(data: T, message: str = "Operation successful") -> 'Result[T]':
        """Create a successful result."""
        return Result(success=True, data=data, message=message)
    
    @staticmethod
    def fail(message: str, errors: Optional[List[ValidationError]] = None) -> 'Result[T]':
        """Create a failed result."""
        return Result(
            success=False, 
            message=message, 
            errors=errors or []
        )
    
    @staticmethod
    def validation_error(field: str, message: str) -> 'Result[T]':
        """Create a validation error result."""
        return Result(
            success=False,
            message="Validation failed",
            errors=[ValidationError(field=field, message=message)]
        )
    
    def add_error(self, field: str, message: str) -> 'Result[T]':
        """Add a validation error to the result."""
        self.errors.append(ValidationError(field=field, message=message))
        return self
