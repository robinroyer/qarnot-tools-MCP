"""Unit tests for authentication adapter.

Tests bearer token validation and header extraction.
"""

import pytest

from src.adapters.auth_adapter import BearerTokenAuth
from src.config.settings import Settings
from src.domain.exceptions import AuthenticationError


class TestBearerTokenAuth:
    """Test suite for BearerTokenAuth adapter."""

    @pytest.mark.unit
    @pytest.mark.auth
    async def test_validate_token_success(
        self, auth_adapter: BearerTokenAuth, test_settings: Settings
    ) -> None:
        """Test successful token validation."""
        result = await auth_adapter.validate_token(test_settings.mcp_auth_token)
        assert result is True

    @pytest.mark.unit
    @pytest.mark.auth
    async def test_validate_token_invalid(self, auth_adapter: BearerTokenAuth) -> None:
        """Test validation with invalid token."""
        with pytest.raises(AuthenticationError, match="Invalid bearer token"):
            await auth_adapter.validate_token("wrong_token")

    @pytest.mark.unit
    @pytest.mark.auth
    async def test_validate_token_empty(self, auth_adapter: BearerTokenAuth) -> None:
        """Test validation with empty token."""
        with pytest.raises(AuthenticationError, match="Bearer token is required"):
            await auth_adapter.validate_token("")

    @pytest.mark.unit
    @pytest.mark.auth
    async def test_validate_token_none(self, auth_adapter: BearerTokenAuth) -> None:
        """Test validation with None token."""
        with pytest.raises(AuthenticationError, match="Bearer token is required"):
            await auth_adapter.validate_token("")  # type: ignore

    @pytest.mark.unit
    @pytest.mark.auth
    def test_extract_token_success(self, auth_adapter: BearerTokenAuth) -> None:
        """Test successful token extraction from header."""
        token = auth_adapter.extract_token_from_header("Bearer test_token_123")
        assert token == "test_token_123"

    @pytest.mark.unit
    @pytest.mark.auth
    def test_extract_token_missing_header(self, auth_adapter: BearerTokenAuth) -> None:
        """Test extraction with missing header."""
        with pytest.raises(
            AuthenticationError, match="Authorization header is required"
        ):
            auth_adapter.extract_token_from_header(None)  # type: ignore

    @pytest.mark.unit
    @pytest.mark.auth
    def test_extract_token_malformed_header(
        self, auth_adapter: BearerTokenAuth
    ) -> None:
        """Test extraction with malformed header."""
        with pytest.raises(AuthenticationError, match="Malformed Authorization header"):
            auth_adapter.extract_token_from_header("InvalidHeader")

    @pytest.mark.unit
    @pytest.mark.auth
    def test_extract_token_wrong_scheme(self, auth_adapter: BearerTokenAuth) -> None:
        """Test extraction with wrong authentication scheme."""
        with pytest.raises(
            AuthenticationError, match="Invalid authentication scheme: Basic"
        ):
            auth_adapter.extract_token_from_header("Basic some_token")

    @pytest.mark.unit
    @pytest.mark.auth
    def test_extract_token_case_insensitive(
        self, auth_adapter: BearerTokenAuth
    ) -> None:
        """Test that Bearer scheme is case insensitive."""
        token = auth_adapter.extract_token_from_header("bearer test_token_123")
        assert token == "test_token_123"
