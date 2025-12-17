"""Main entry point for the Qarnot MCP Server.

This module initializes all components and starts the MCP server.
"""

import json
import logging
import sys
from typing import Any

from src.adapters.auth_adapter import BearerTokenAuth
from src.adapters.mcp_adapter import MCPAdapter
from src.adapters.qarnot_adapter import QarnotAdapter
from src.config.settings import Settings
from src.domain.use_cases.cancel_job_usecase import CancelJobUseCase
from src.domain.use_cases.get_job_status_usecase import GetJobStatusUseCase
from src.domain.use_cases.list_jobs_usecase import ListJobsUseCase
from src.domain.use_cases.retrieve_results_usecase import RetrieveResultsUseCase
from src.domain.use_cases.submit_job_usecase import SubmitJobUseCase


def setup_logging(settings: Settings) -> None:
    """Configure logging based on settings.

    Args:
        settings: Application settings with log level and format
    """
    log_level = getattr(logging, settings.log_level.upper())

    if settings.log_format == "json":
        # JSON formatter for production
        class JsonFormatter(logging.Formatter):
            def format(self, record: logging.LogRecord) -> str:
                log_data: dict[str, Any] = {
                    "timestamp": self.formatTime(record, self.datefmt),
                    "level": record.levelname,
                    "logger": record.name,
                    "message": record.getMessage(),
                }

                if hasattr(record, "extra"):
                    log_data.update(record.extra)

                if record.exc_info:
                    log_data["exception"] = self.formatException(record.exc_info)

                return json.dumps(log_data)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
    else:
        # Text formatter for development
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=[handler],
        force=True,
    )

    logger = logging.getLogger(__name__)
    logger.info(
        "Logging configured",
        extra={"level": settings.log_level, "format": settings.log_format}
    )


def create_app() -> MCPAdapter:
    """Create and configure the MCP application.

    This function implements dependency injection, wiring all components
    together following hexagonal architecture principles.

    Returns:
        Configured MCP adapter ready to serve requests
    """
    logger = logging.getLogger(__name__)
    logger.info("Initializing Qarnot MCP Server")

    # Load settings from environment
    settings = Settings()
    logger.info("Settings loaded from environment")

    # Initialize adapters (infrastructure layer)
    auth = BearerTokenAuth(settings)
    qarnot_client = QarnotAdapter(settings)

    # Initialize use cases (application layer)
    submit_job_uc = SubmitJobUseCase(qarnot_client)
    get_status_uc = GetJobStatusUseCase(qarnot_client)
    retrieve_results_uc = RetrieveResultsUseCase(qarnot_client)
    cancel_job_uc = CancelJobUseCase(qarnot_client)
    list_jobs_uc = ListJobsUseCase(qarnot_client)

    # Initialize MCP adapter (presentation layer)
    mcp_adapter = MCPAdapter(
        auth=auth,
        submit_job_uc=submit_job_uc,
        get_status_uc=get_status_uc,
        retrieve_results_uc=retrieve_results_uc,
        cancel_job_uc=cancel_job_uc,
        list_jobs_uc=list_jobs_uc,
    )

    logger.info("Qarnot MCP Server initialized successfully")
    return mcp_adapter


def main() -> None:
    """Main entry point for the application."""
    # Load settings first to configure logging
    settings = Settings()
    setup_logging(settings)

    logger = logging.getLogger(__name__)

    try:
        # Create and configure the application
        mcp_adapter = create_app()
        mcp_app = mcp_adapter.get_app()

        logger.info(
            "Starting MCP server",
            extra={
                "host": settings.mcp_host,
                "port": settings.mcp_port,
            }
        )

        # Run the FastMCP server
        # FastMCP will handle HTTP server startup with Uvicorn
        mcp_app.run(
            transport="sse",  # Server-Sent Events transport for HTTP
            host=settings.mcp_host,
            port=settings.mcp_port,
        )

    except KeyboardInterrupt:
        logger.info("Received shutdown signal, stopping server")
        sys.exit(0)

    except Exception as e:
        logger.critical(
            "Fatal error starting server",
            exc_info=e
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
