"""Authentication port (interface) for hexagonal architecture.

This module defines the abstract interface for authentication services.
Concrete implementations will handle bearer token validation.
"""

from abc import ABC, abstractmethod


class AuthPort(ABC):
    """Abstract interface for authentication operations.

    This port defines the contract for authentication adapters.
    Implementations must provide bearer token validation.
    """

    @abstractmethod
    async def validate_token(self, token: str) -> bool:
        """Validate a bearer token.

        Args:
            token: The bearer token to validate (without "Bearer " prefix)

        Returns:
            True if token is valid

        Raises:
            AuthenticationError: If token is invalid or expired
        """
        pass
