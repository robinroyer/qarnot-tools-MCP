"""Configuration module for Qarnot MCP Server.

This module defines the application settings using Pydantic Settings,
loading configuration from environment variables.
"""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    All sensitive values (tokens, API keys) must be provided via
    environment variables and never hardcoded.
    """

    # MCP Server Settings
    mcp_auth_token: str = Field(
        description="Bearer token for MCP server authentication"
    )
    mcp_host: str = Field(
        default="0.0.0.0", description="Host to bind the MCP server to"
    )
    mcp_port: int = Field(
        default=3000, description="Port to bind the MCP server to", ge=1, le=65535
    )

    # Qarnot Cloud Settings
    qarnot_api_token: str = Field(
        description="API token for Qarnot Cloud authentication"
    )
    qarnot_api_url: str = Field(
        default="https://api.qarnot.com", description="Qarnot API base URL"
    )

    # Logging Settings
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )
    log_format: Literal["json", "text"] = Field(
        default="json", description="Logging format (json for production, text for dev)"
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )
