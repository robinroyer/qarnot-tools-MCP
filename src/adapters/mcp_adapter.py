"""MCP adapter implementation using FastMCP.

This module implements the MCP server that exposes Qarnot operations
as MCP tools for LLM consumption.
"""

import logging
from typing import Any

from fastmcp import FastMCP

from src.domain.use_cases.cancel_job_usecase import CancelJobUseCase
from src.domain.use_cases.get_job_status_usecase import GetJobStatusUseCase
from src.domain.use_cases.list_jobs_usecase import ListJobsUseCase
from src.domain.use_cases.retrieve_results_usecase import RetrieveResultsUseCase
from src.domain.use_cases.submit_job_usecase import SubmitJobUseCase
from src.ports.auth_port import AuthPort
from src.schemas.inputs import (
    CancelJobRequest,
    GetJobStatusRequest,
    ListJobsRequest,
    RetrieveResultsRequest,
    SubmitJobRequest,
)
from src.schemas.outputs import (
    JobCancelled,
    JobResults,
    JobStatus,
    JobSubmitted,
    JobSummary,
    JobsList,
)

logger = logging.getLogger(__name__)


class MCPAdapter:
    """MCP Server adapter using FastMCP.

    This adapter exposes use cases as MCP tools with proper
    authentication and error handling.
    """

    def __init__(
        self,
        auth: AuthPort,
        submit_job_uc: SubmitJobUseCase,
        get_status_uc: GetJobStatusUseCase,
        retrieve_results_uc: RetrieveResultsUseCase,
        cancel_job_uc: CancelJobUseCase,
        list_jobs_uc: ListJobsUseCase,
    ):
        """Initialize the MCP adapter.

        Args:
            auth: Authentication port for token validation
            submit_job_uc: Use case for submitting jobs
            get_status_uc: Use case for getting job status
            retrieve_results_uc: Use case for retrieving results
            cancel_job_uc: Use case for cancelling jobs
            list_jobs_uc: Use case for listing jobs
        """
        self.auth = auth
        self.submit_job_uc = submit_job_uc
        self.get_status_uc = get_status_uc
        self.retrieve_results_uc = retrieve_results_uc
        self.cancel_job_uc = cancel_job_uc
        self.list_jobs_uc = list_jobs_uc

        # Initialize FastMCP server
        self.mcp = FastMCP("Qarnot Computing MCP Server")
        self._register_tools()

        logger.info("MCP adapter initialized")

    def _register_tools(self) -> None:
        """Register all MCP tools with the FastMCP server."""

        @self.mcp.tool(
            description="Submit a new computational job to Qarnot Computing",
            destructive=True,
        )
        async def submit_job(request: dict[str, Any]) -> dict[str, Any]:
            """Submit a new job to Qarnot Computing.

            Args:
                request: Job submission request with name, config, etc.

            Returns:
                Job submission result with job_id and status
            """
            logger.info("MCP tool called: submit_job")

            # Validate input
            validated_input = SubmitJobRequest(**request)

            # Execute use case
            job = await self.submit_job_uc.execute(
                name=validated_input.job_name,
                config=validated_input.job_config,
                instance_count=validated_input.instance_count,
                resource_type=validated_input.resource_type,
                priority=validated_input.priority,
                tags=validated_input.tags,
            )

            # Map to output schema
            output = JobSubmitted(
                job_id=job.job_id,
                status=job.status,
                name=job.name,
                created_at=job.created_at,
                instance_count=job.instance_count,
                resource_type=job.resource_type,
            )

            return output.model_dump(mode="json")

        @self.mcp.tool(
            description="Get the current status of a Qarnot job",
            read_only=True,
        )
        async def get_job_status(request: dict[str, Any]) -> dict[str, Any]:
            """Get the current status of a job.

            Args:
                request: Request with job_id

            Returns:
                Job status with progress and timestamps
            """
            logger.info("MCP tool called: get_job_status")

            # Validate input
            validated_input = GetJobStatusRequest(**request)

            # Execute use case
            job = await self.get_status_uc.execute(validated_input.job_id)

            # Map to output schema
            output = JobStatus(
                job_id=job.job_id,
                status=job.status,
                progress=job.progress,
                started_at=job.started_at,
                updated_at=job.updated_at,
                error_message=job.error_message,
            )

            return output.model_dump(mode="json")

        @self.mcp.tool(
            description="Retrieve results from a completed Qarnot job",
            read_only=True,
        )
        async def retrieve_job_results(request: dict[str, Any]) -> dict[str, Any]:
            """Retrieve results from a completed job.

            Args:
                request: Request with job_id and optional output_path

            Returns:
                Job results metadata with download URLs
            """
            logger.info("MCP tool called: retrieve_job_results")

            # Validate input
            validated_input = RetrieveResultsRequest(**request)

            # Execute use case
            result = await self.retrieve_results_uc.execute(
                job_id=validated_input.job_id,
                output_path=validated_input.output_path,
            )

            # Map to output schema
            output = JobResults(
                job_id=result.job_id,
                status=result.status,
                results_url=result.results_url,
                file_size_bytes=result.file_size_bytes,
                file_count=result.file_count,
                download_url=result.download_url,
            )

            return output.model_dump(mode="json")

        @self.mcp.tool(
            description="Cancel a running Qarnot job",
            destructive=True,
        )
        async def cancel_job(request: dict[str, Any]) -> dict[str, Any]:
            """Cancel a running job.

            Args:
                request: Request with job_id and optional reason

            Returns:
                Cancellation confirmation with timestamp
            """
            logger.info("MCP tool called: cancel_job")

            # Validate input
            validated_input = CancelJobRequest(**request)

            # Execute use case
            job = await self.cancel_job_uc.execute(
                job_id=validated_input.job_id,
                reason=validated_input.reason,
            )

            # Map to output schema
            output = JobCancelled(
                job_id=job.job_id,
                cancelled_at=job.updated_at,
                status=job.status,
                reason=validated_input.reason,
            )

            return output.model_dump(mode="json")

        @self.mcp.tool(
            description="List jobs for the authenticated user",
            read_only=True,
        )
        async def list_jobs(request: dict[str, Any]) -> dict[str, Any]:
            """List jobs with optional filtering and pagination.

            Args:
                request: Request with limit, offset, and status_filter

            Returns:
                List of jobs with pagination info
            """
            logger.info("MCP tool called: list_jobs")

            # Validate input
            validated_input = ListJobsRequest(**request)

            # Execute use case
            jobs, total_count, next_offset = await self.list_jobs_uc.execute(
                limit=validated_input.limit,
                offset=validated_input.offset,
                status_filter=validated_input.status_filter,
            )

            # Map to output schema
            job_summaries = [
                JobSummary(
                    job_id=job.job_id,
                    status=job.status,
                    name=job.name,
                    created_at=job.created_at,
                )
                for job in jobs
            ]

            output = JobsList(
                total_count=total_count,
                jobs=job_summaries,
                next_offset=next_offset,
            )

            return output.model_dump(mode="json")

        logger.info("All MCP tools registered")

    def get_app(self) -> FastMCP:
        """Get the FastMCP application instance.

        Returns:
            The FastMCP application
        """
        return self.mcp
