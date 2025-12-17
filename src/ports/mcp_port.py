"""MCP Server port (interface) for hexagonal architecture.

This module defines the abstract interface for MCP server operations.
Concrete implementations will use FastMCP to expose tools.
"""

from abc import ABC, abstractmethod


class MCPPort(ABC):
    """Abstract interface for MCP server operations.

    This port defines the contract for MCP adapters.
    Implementations must expose use cases as MCP tools.
    """

    @abstractmethod
    async def start(self) -> None:
        """Start the MCP server.

        Raises:
            RuntimeError: If server fails to start
        """
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stop the MCP server gracefully.

        Raises:
            RuntimeError: If server fails to stop
        """
        pass

    @abstractmethod
    def register_tools(self) -> None:
        """Register all MCP tools with the server.

        This method should register all use cases as MCP tools
        with proper schemas and annotations.
        """
        pass
