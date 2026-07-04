"""Domain exceptions for AlphaHunter AI."""


class AlphaHunterError(Exception):
    """Base exception for all AlphaHunter AI errors."""

    def __init__(self, message: str, details: dict | None = None) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            details: Optional dictionary with additional context.
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConfigurationError(AlphaHunterError):
    """Raised when application configuration is invalid or missing."""


class DatabaseError(AlphaHunterError):
    """Raised when a database operation fails."""


class ProviderError(AlphaHunterError):
    """Raised when a data provider operation fails."""


class ValidationError(AlphaHunterError):
    """Raised when input validation fails."""
