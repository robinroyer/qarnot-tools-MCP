"""Custom exceptions for the Qarnot MCP Server.

This module defines domain-specific exceptions for clear error handling
and messaging throughout the application.
"""


class QarnotMCPError(Exception):
    """Base exception for all Qarnot MCP Server errors."""

    pass


# Authentication Errors
class AuthenticationError(QarnotMCPError):
    """Raised when authentication fails."""

    pass


# Qarnot API Errors
class QarnotAPIError(QarnotMCPError):
    """Base exception for Qarnot API errors."""

    pass


class JobNotFoundError(QarnotAPIError):
    """Raised when a job cannot be found."""

    def __init__(self, job_id: str):
        """Initialize with job ID.

        Args:
            job_id: The ID of the job that wasn't found
        """
        super().__init__(f"Job not found: {job_id}")
        self.job_id = job_id


class JobNotCompletedError(QarnotAPIError):
    """Raised when attempting to retrieve results from incomplete job."""

    def __init__(self, job_id: str, current_status: str):
        """Initialize with job ID and status.

        Args:
            job_id: The ID of the job
            current_status: Current status of the job
        """
        super().__init__(
            f"Job {job_id} has not completed yet. Current status: {current_status}"
        )
        self.job_id = job_id
        self.current_status = current_status


class JobAlreadyCompletedError(QarnotAPIError):
    """Raised when attempting to cancel an already completed job."""

    def __init__(self, job_id: str, current_status: str):
        """Initialize with job ID and status.

        Args:
            job_id: The ID of the job
            current_status: Current status of the job
        """
        super().__init__(
            f"Job {job_id} has already completed. Current status: {current_status}"
        )
        self.job_id = job_id
        self.current_status = current_status


class QarnotConnectionError(QarnotAPIError):
    """Raised when connection to Qarnot API fails."""

    pass


class QarnotTimeoutError(QarnotAPIError):
    """Raised when Qarnot API request times out."""

    pass


# Validation Errors
class ValidationError(QarnotMCPError):
    """Raised when input validation fails."""

    pass


# MCP Server Errors
class MCPServerError(QarnotMCPError):
    """Base exception for MCP server errors."""

    pass


class MCPServerStartupError(MCPServerError):
    """Raised when MCP server fails to start."""

    pass


class MCPServerShutdownError(MCPServerError):
    """Raised when MCP server fails to shut down gracefully."""

    pass
