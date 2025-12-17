"""Pytest configuration and shared fixtures.

This module provides common fixtures for all tests.
"""

from datetime import datetime
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.adapters.auth_adapter import BearerTokenAuth
from src.adapters.qarnot_adapter import QarnotAdapter
from src.config.settings import Settings
from src.domain.entities.job import Job
from src.domain.entities.job_result import JobResult
from src.domain.use_cases.cancel_job_usecase import CancelJobUseCase
from src.domain.use_cases.get_job_status_usecase import GetJobStatusUseCase
from src.domain.use_cases.list_jobs_usecase import ListJobsUseCase
from src.domain.use_cases.retrieve_results_usecase import RetrieveResultsUseCase
from src.domain.use_cases.submit_job_usecase import SubmitJobUseCase
from src.ports.qarnot_port import QarnotPort


@pytest.fixture
def test_settings() -> Settings:
    """Provide test settings.

    Returns:
        Settings instance with test values
    """
    return Settings(
        mcp_auth_token="test_token_123",
        mcp_host="127.0.0.1",
        mcp_port=3000,
        qarnot_api_token="test_qarnot_token",
        qarnot_api_url="https://api.test.qarnot.com",
        log_level="DEBUG",
        log_format="text",
    )


@pytest.fixture
def auth_adapter(test_settings: Settings) -> BearerTokenAuth:
    """Provide authentication adapter.

    Args:
        test_settings: Test settings fixture

    Returns:
        BearerTokenAuth instance
    """
    return BearerTokenAuth(test_settings)


@pytest.fixture
def mock_qarnot_client() -> AsyncMock:
    """Provide a mock Qarnot client.

    Returns:
        AsyncMock implementing QarnotPort interface
    """
    mock = AsyncMock(spec=QarnotPort)
    return mock


@pytest.fixture
def sample_job() -> Job:
    """Provide a sample job entity.

    Returns:
        Job entity for testing
    """
    now = datetime.utcnow()
    return Job(
        job_id="job-test-123",
        name="test-job",
        status="running",
        instance_count=4,
        resource_type="CPU",
        priority=10,
        tags=["test", "sample"],
        config={"docker_image": "python:3.11"},
        created_at=now,
        started_at=now,
        updated_at=now,
        progress=50.0,
    )


@pytest.fixture
def sample_job_result() -> JobResult:
    """Provide a sample job result entity.

    Returns:
        JobResult entity for testing
    """
    return JobResult(
        job_id="job-test-123",
        status="completed",
        results_url="https://storage.test.qarnot.com/results/job-test-123",
        file_size_bytes=1048576,
        file_count=5,
        download_url="https://storage.test.qarnot.com/download/xyz",
        checksum="sha256:abc123",
    )


@pytest.fixture
def submit_job_usecase(mock_qarnot_client: AsyncMock) -> SubmitJobUseCase:
    """Provide submit job use case with mock client.

    Args:
        mock_qarnot_client: Mock Qarnot client fixture

    Returns:
        SubmitJobUseCase instance
    """
    return SubmitJobUseCase(mock_qarnot_client)


@pytest.fixture
def get_status_usecase(mock_qarnot_client: AsyncMock) -> GetJobStatusUseCase:
    """Provide get status use case with mock client.

    Args:
        mock_qarnot_client: Mock Qarnot client fixture

    Returns:
        GetJobStatusUseCase instance
    """
    return GetJobStatusUseCase(mock_qarnot_client)


@pytest.fixture
def retrieve_results_usecase(
    mock_qarnot_client: AsyncMock,
) -> RetrieveResultsUseCase:
    """Provide retrieve results use case with mock client.

    Args:
        mock_qarnot_client: Mock Qarnot client fixture

    Returns:
        RetrieveResultsUseCase instance
    """
    return RetrieveResultsUseCase(mock_qarnot_client)


@pytest.fixture
def cancel_job_usecase(mock_qarnot_client: AsyncMock) -> CancelJobUseCase:
    """Provide cancel job use case with mock client.

    Args:
        mock_qarnot_client: Mock Qarnot client fixture

    Returns:
        CancelJobUseCase instance
    """
    return CancelJobUseCase(mock_qarnot_client)


@pytest.fixture
def list_jobs_usecase(mock_qarnot_client: AsyncMock) -> ListJobsUseCase:
    """Provide list jobs use case with mock client.

    Args:
        mock_qarnot_client: Mock Qarnot client fixture

    Returns:
        ListJobsUseCase instance
    """
    return ListJobsUseCase(mock_qarnot_client)
