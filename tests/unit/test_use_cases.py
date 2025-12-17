"""Unit tests for use cases.

Tests business logic in use cases with mocked dependencies.
"""

from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.domain.entities.job import Job
from src.domain.entities.job_result import JobResult
from src.domain.exceptions import JobNotFoundError
from src.domain.use_cases.cancel_job_usecase import CancelJobUseCase
from src.domain.use_cases.get_job_status_usecase import GetJobStatusUseCase
from src.domain.use_cases.list_jobs_usecase import ListJobsUseCase
from src.domain.use_cases.retrieve_results_usecase import RetrieveResultsUseCase
from src.domain.use_cases.submit_job_usecase import SubmitJobUseCase
from tests.fixtures.mock_qarnot_responses import create_mock_job, create_mock_job_list


class TestSubmitJobUseCase:
    """Test suite for SubmitJobUseCase."""

    @pytest.mark.unit
    async def test_execute_success(
        self,
        submit_job_usecase: SubmitJobUseCase,
        mock_qarnot_client: AsyncMock,
        sample_job: Job,
    ) -> None:
        """Test successful job submission."""
        mock_qarnot_client.submit_job.return_value = sample_job

        result = await submit_job_usecase.execute(
            name="test-job",
            config={"docker_image": "python:3.11"},
            instance_count=4,
            resource_type="CPU",
            priority=10,
            tags=["test"],
        )

        assert result.job_id == sample_job.job_id
        assert result.name == sample_job.name
        mock_qarnot_client.submit_job.assert_called_once()

    @pytest.mark.unit
    async def test_execute_propagates_errors(
        self,
        submit_job_usecase: SubmitJobUseCase,
        mock_qarnot_client: AsyncMock,
    ) -> None:
        """Test that errors from client are propagated."""
        mock_qarnot_client.submit_job.side_effect = Exception("API Error")

        with pytest.raises(Exception, match="API Error"):
            await submit_job_usecase.execute(
                name="test-job",
                config={},
                instance_count=1,
                resource_type="CPU",
            )


class TestGetJobStatusUseCase:
    """Test suite for GetJobStatusUseCase."""

    @pytest.mark.unit
    async def test_execute_success(
        self,
        get_status_usecase: GetJobStatusUseCase,
        mock_qarnot_client: AsyncMock,
        sample_job: Job,
    ) -> None:
        """Test successful status retrieval."""
        mock_qarnot_client.get_job_status.return_value = sample_job

        result = await get_status_usecase.execute("job-test-123")

        assert result.job_id == sample_job.job_id
        assert result.status == sample_job.status
        mock_qarnot_client.get_job_status.assert_called_once_with("job-test-123")

    @pytest.mark.unit
    async def test_execute_job_not_found(
        self,
        get_status_usecase: GetJobStatusUseCase,
        mock_qarnot_client: AsyncMock,
    ) -> None:
        """Test status retrieval for non-existent job."""
        mock_qarnot_client.get_job_status.side_effect = JobNotFoundError("job-123")

        with pytest.raises(JobNotFoundError):
            await get_status_usecase.execute("job-123")


class TestRetrieveResultsUseCase:
    """Test suite for RetrieveResultsUseCase."""

    @pytest.mark.unit
    async def test_execute_success(
        self,
        retrieve_results_usecase: RetrieveResultsUseCase,
        mock_qarnot_client: AsyncMock,
        sample_job_result: JobResult,
    ) -> None:
        """Test successful results retrieval."""
        mock_qarnot_client.retrieve_results.return_value = sample_job_result

        result = await retrieve_results_usecase.execute("job-test-123")

        assert result.job_id == sample_job_result.job_id
        assert result.file_count == sample_job_result.file_count
        mock_qarnot_client.retrieve_results.assert_called_once_with(
            "job-test-123", None
        )

    @pytest.mark.unit
    async def test_execute_with_output_path(
        self,
        retrieve_results_usecase: RetrieveResultsUseCase,
        mock_qarnot_client: AsyncMock,
        sample_job_result: JobResult,
    ) -> None:
        """Test results retrieval with output path."""
        mock_qarnot_client.retrieve_results.return_value = sample_job_result

        result = await retrieve_results_usecase.execute(
            "job-test-123", output_path="/tmp/results"
        )

        assert result.job_id == sample_job_result.job_id
        mock_qarnot_client.retrieve_results.assert_called_once_with(
            "job-test-123", "/tmp/results"
        )


class TestCancelJobUseCase:
    """Test suite for CancelJobUseCase."""

    @pytest.mark.unit
    async def test_execute_success(
        self,
        cancel_job_usecase: CancelJobUseCase,
        mock_qarnot_client: AsyncMock,
        sample_job: Job,
    ) -> None:
        """Test successful job cancellation."""
        cancelled_job = create_mock_job(job_id="job-test-123", status="cancelled")
        mock_qarnot_client.cancel_job.return_value = cancelled_job

        result = await cancel_job_usecase.execute("job-test-123", reason="Test cancel")

        assert result.job_id == "job-test-123"
        assert result.status == "cancelled"
        mock_qarnot_client.cancel_job.assert_called_once_with(
            "job-test-123", "Test cancel"
        )


class TestListJobsUseCase:
    """Test suite for ListJobsUseCase."""

    @pytest.mark.unit
    async def test_execute_success(
        self,
        list_jobs_usecase: ListJobsUseCase,
        mock_qarnot_client: AsyncMock,
    ) -> None:
        """Test successful job listing."""
        mock_jobs = create_mock_job_list(count=3)
        mock_qarnot_client.list_jobs.return_value = (mock_jobs, 10)

        jobs, total, next_offset = await list_jobs_usecase.execute(limit=3, offset=0)

        assert len(jobs) == 3
        assert total == 10
        assert next_offset == 3  # offset + limit
        mock_qarnot_client.list_jobs.assert_called_once_with(
            limit=3, offset=0, status_filter=None
        )

    @pytest.mark.unit
    async def test_execute_last_page(
        self,
        list_jobs_usecase: ListJobsUseCase,
        mock_qarnot_client: AsyncMock,
    ) -> None:
        """Test listing last page (no next_offset)."""
        mock_jobs = create_mock_job_list(count=2)
        mock_qarnot_client.list_jobs.return_value = (mock_jobs, 12)

        jobs, total, next_offset = await list_jobs_usecase.execute(limit=10, offset=10)

        assert len(jobs) == 2
        assert total == 12
        assert next_offset is None  # No more pages
        mock_qarnot_client.list_jobs.assert_called_once()

    @pytest.mark.unit
    async def test_execute_with_filter(
        self,
        list_jobs_usecase: ListJobsUseCase,
        mock_qarnot_client: AsyncMock,
    ) -> None:
        """Test listing with status filter."""
        mock_jobs = [create_mock_job(status="running")]
        mock_qarnot_client.list_jobs.return_value = (mock_jobs, 1)

        jobs, total, next_offset = await list_jobs_usecase.execute(
            limit=10, offset=0, status_filter="running"
        )

        assert len(jobs) == 1
        assert jobs[0].status == "running"
        mock_qarnot_client.list_jobs.assert_called_once_with(
            limit=10, offset=0, status_filter="running"
        )
