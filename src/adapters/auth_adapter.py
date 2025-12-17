"""Authentication adapter implementation.

This module implements bearer token authentication for the MCP server.
It uses timing-safe comparison to prevent timing attacks.
"""

import logging
import secrets
from typing import Optional

from src.config.settings import Settings
from src.domain.exceptions import AuthenticationError
from src.ports.auth_port import AuthPort

logger = logging.getLogger(__name__)


class BearerTokenAuth(AuthPort):
    """Bearer token authentication implementation.

    This adapter validates bearer tokens against a configured secret token.
    Uses constant-time comparison to prevent timing attacks.

    Attributes:
        _valid_token: The expected bearer token (from settings)
    """

    def __init__(self, settings: Settings):
        """Initialize the authentication adapter.

        Args:
            settings: Application settings containing the auth token
        """
        self._valid_token = settings.mcp_auth_token
        logger.info("Bearer token authentication initialized")

    async def validate_token(self, token: str) -> bool:
        """Validate a bearer token using constant-time comparison.

        Args:
            token: The bearer token to validate (without "Bearer " prefix)

        Returns:
            True if token is valid

        Raises:
            AuthenticationError: If token is invalid, missing, or empty

        Example:
            >>> auth = BearerTokenAuth(settings)
            >>> await auth.validate_token("valid_token_here")
            True
        """
        if not token:
            logger.warning("Authentication attempt with empty token")
            raise AuthenticationError("Bearer token is required")

        # Use constant-time comparison to prevent timing attacks
        if not secrets.compare_digest(token, self._valid_token):
            logger.warning(
                "Authentication failed: invalid token",
                extra={"token_prefix": token[:8] if len(token) >= 8 else "***"}
            )
            raise AuthenticationError("Invalid bearer token")

        logger.debug("Authentication successful")
        return True

    def extract_token_from_header(self, authorization_header: Optional[str]) -> str:
        """Extract bearer token from Authorization header.

        Args:
            authorization_header: The Authorization header value

        Returns:
            The extracted token (without "Bearer " prefix)

        Raises:
            AuthenticationError: If header is missing or malformed

        Example:
            >>> auth = BearerTokenAuth(settings)
            >>> token = auth.extract_token_from_header("Bearer abc123")
            >>> # token == "abc123"
        """
        if not authorization_header:
            logger.warning("Missing Authorization header")
            raise AuthenticationError("Authorization header is required")

        parts = authorization_header.split()

        if len(parts) != 2:
            logger.warning(
                "Malformed Authorization header",
                extra={"parts_count": len(parts)}
            )
            raise AuthenticationError("Malformed Authorization header")

        scheme, token = parts

        if scheme.lower() != "bearer":
            logger.warning(
                "Invalid authentication scheme",
                extra={"scheme": scheme}
            )
            raise AuthenticationError(
                f"Invalid authentication scheme: {scheme}. Expected 'Bearer'"
            )

        return token
