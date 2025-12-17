"""Integration tests for MCP server.

Tests end-to-end MCP server functionality including tool calls
and authentication.
"""

from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock

import pytest

from src.adapters.auth_adapter import BearerTokenAuth
from src.adapters.mcp_adapter import MCPAdapter
from src.adapters.qarnot_adapter import QarnotAdapter
from src.config.settings import Settings
from src.domain.use_cases.cancel_job_usecase import CancelJobUseCase
from src.domain.use_cases.get_job_status_usecase import GetJobStatusUseCase
from src.domain.use_cases.list_jobs_usecase import ListJobsUseCase
from src.domain.use_cases.retrieve_results_usecase import RetrieveResultsUseCase
from src.domain.use_cases.submit_job_usecase import SubmitJobUseCase
from tests.fixtures.mock_qarnot_responses import (
    create_mock_job,
    create_mock_job_list,
    create_mock_job_result,
)


@pytest.fixture
def mcp_adapter_with_mocks(
    test_settings: Settings,
    mock_qarnot_client: AsyncMock,
) -> MCPAdapter:
    """Provide MCP adapter with mocked dependencies.

    Args:
        test_settings: Test settings fixture
        mock_qarnot_client: Mock Qarnot client fixture

    Returns:
        MCPAdapter instance with mocked Qarnot client
    """
    auth = BearerTokenAuth(test_settings)

    # Create use cases with mock client
    submit_job_uc = SubmitJobUseCase(mock_qarnot_client)
    get_status_uc = GetJobStatusUseCase(mock_qarnot_client)
    retrieve_results_uc = RetrieveResultsUseCase(mock_qarnot_client)
    cancel_job_uc = CancelJobUseCase(mock_qarnot_client)
    list_jobs_uc = ListJobsUseCase(mock_qarnot_client)

    # Create MCP adapter
    return MCPAdapter(
        auth=auth,
        submit_job_uc=submit_job_uc,
        get_status_uc=get_status_uc,
        retrieve_results_uc=retrieve_results_uc,
        cancel_job_uc=cancel_job_uc,
        list_jobs_uc=list_jobs_uc,
    )


class TestMCPServerIntegration:
    """Integration test suite for MCP server."""

    @pytest.mark.integration
    async def test_mcp_adapter_initialization(
        self, mcp_adapter_with_mocks: MCPAdapter
    ) -> None:
        """Test MCP adapter initializes correctly."""
        assert mcp_adapter_with_mocks.mcp is not None
        assert mcp_adapter_with_mocks.auth is not None

    @pytest.mark.integration
    async def test_submit_job_tool_end_to_end(
        self,
        mcp_adapter_with_mocks: MCPAdapter,
        mock_qarnot_client: AsyncMock,
    ) -> None:
        """Test submit_job tool end-to-end."""
        # Setup mock
        mock_job = create_mock_job(job_id="job-integration-123", status="submitted")
        mock_qarnot_client.submit_job.return_value = mock_job

        # Get the tool function (this is simplified - actual MCP invocation would be different)
        # In practice, you'd use MCP client to call the tool
        # This test validates the use case integration

        result = await mcp_adapter_with_mocks.submit_job_uc.execute(
            name="integration-test-job",
            config={"docker_image": "python:3.11"},
            instance_count=2,
            resource_type="CPU",
            priority=5,
            tags=["integration", "test"],
        )

        assert result.job_id == "job-integration-123"
        assert result.status == "submitted"
        mock_qarnot_client.submit_job.assert_called_once()

    @pytest.mark.integration
    async def test_get_job_status_tool_end_to_end(
        self,
        mcp_adapter_with_mocks: MCPAdapter,
        mock_qarnot_client: AsyncMock,
    ) -> None:
        """Test get_job_status tool end-to-end."""
        # Setup mock
        mock_job = create_mock_job(
            job_id="job-status-123", status="running", progress=75.0
        )
        mock_qarnot_client.get_job_status.return_value = mock_job

        # Execute use case
        result = await mcp_adapter_with_mocks.get_status_uc.execute("job-status-123")

        assert result.job_id == "job-status-123"
        assert result.status == "running"
        assert result.progress == 75.0
        mock_qarnot_client.get_job_status.assert_called_once_with("job-status-123")

    @pytest.mark.integration
    async def test_retrieve_results_tool_end_to_end(
        self,
        mcp_adapter_with_mocks: MCPAdapter,
        mock_qarnot_client: AsyncMock,
    ) -> None:
        """Test retrieve_job_results tool end-to-end."""
        # Setup mock
        mock_result = create_mock_job_result(job_id="job-results-123")
        mock_qarnot_client.retrieve_results.return_value = mock_result

        # Execute use case
        result = await mcp_adapter_with_mocks.retrieve_results_uc.execute(
            "job-results-123", output_path="/tmp/results"
        )

        assert result.job_id == "job-results-123"
        assert result.status == "completed"
        assert result.file_count > 0
        mock_qarnot_client.retrieve_results.assert_called_once_with(
            "job-results-123", "/tmp/results"
        )

    @pytest.mark.integration
    async def test_cancel_job_tool_end_to_end(
        self,
        mcp_adapter_with_mocks: MCPAdapter,
        mock_qarnot_client: AsyncMock,
    ) -> None:
        """Test cancel_job tool end-to-end."""
        # Setup mock
        mock_job = create_mock_job(job_id="job-cancel-123", status="cancelled")
        mock_qarnot_client.cancel_job.return_value = mock_job

        # Execute use case
        result = await mcp_adapter_with_mocks.cancel_job_uc.execute(
            "job-cancel-123", reason="Integration test cancellation"
        )

        assert result.job_id == "job-cancel-123"
        assert result.status == "cancelled"
        mock_qarnot_client.cancel_job.assert_called_once()

    @pytest.mark.integration
    async def test_list_jobs_tool_end_to_end(
        self,
        mcp_adapter_with_mocks: MCPAdapter,
        mock_qarnot_client: AsyncMock,
    ) -> None:
        """Test list_jobs tool end-to-end."""
        # Setup mock
        mock_jobs = create_mock_job_list(count=5)
        mock_qarnot_client.list_jobs.return_value = (mock_jobs, 20)

        # Execute use case
        jobs, total, next_offset = await mcp_adapter_with_mocks.list_jobs_uc.execute(
            limit=5, offset=0, status_filter="running"
        )

        assert len(jobs) == 5
        assert total == 20
        assert next_offset == 5
        mock_qarnot_client.list_jobs.assert_called_once()

    @pytest.mark.integration
    async def test_mcp_adapter_with_all_use_cases(
        self,
        test_settings: Settings,
    ) -> None:
        """Test MCP adapter integrates all use cases correctly."""
        # Create real adapter (with mock Qarnot client)
        mock_qarnot = AsyncMock()
        auth = BearerTokenAuth(test_settings)

        submit_uc = SubmitJobUseCase(mock_qarnot)
        status_uc = GetJobStatusUseCase(mock_qarnot)
        results_uc = RetrieveResultsUseCase(mock_qarnot)
        cancel_uc = CancelJobUseCase(mock_qarnot)
        list_uc = ListJobsUseCase(mock_qarnot)

        adapter = MCPAdapter(
            auth=auth,
            submit_job_uc=submit_uc,
            get_status_uc=status_uc,
            retrieve_results_uc=results_uc,
            cancel_job_uc=cancel_uc,
            list_jobs_uc=list_uc,
        )

        # Verify adapter has all components
        assert adapter.auth is not None
        assert adapter.submit_job_uc is not None
        assert adapter.get_status_uc is not None
        assert adapter.retrieve_results_uc is not None
        assert adapter.cancel_job_uc is not None
        assert adapter.list_jobs_uc is not None
        assert adapter.mcp is not None
