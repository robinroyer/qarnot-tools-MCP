"""Unit tests for Pydantic schemas.

Tests input and output schema validation.
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

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


class TestInputSchemas:
    """Test suite for input schemas."""

    @pytest.mark.unit
    def test_submit_job_request_valid(self) -> None:
        """Test valid submit job request."""
        request = SubmitJobRequest(
            job_name="test-job",
            job_config={"docker_image": "python:3.11"},
            instance_count=4,
            resource_type="CPU",
            priority=10,
            tags=["test"],
        )

        assert request.job_name == "test-job"
        assert request.instance_count == 4
        assert request.resource_type == "CPU"

    @pytest.mark.unit
    def test_submit_job_request_invalid_resource_type(self) -> None:
        """Test submit job request with invalid resource type."""
        with pytest.raises(ValidationError):
            SubmitJobRequest(
                job_name="test-job",
                job_config={},
                instance_count=4,
                resource_type="INVALID",  # Should be CPU or GPU
            )

    @pytest.mark.unit
    def test_submit_job_request_invalid_instance_count(self) -> None:
        """Test submit job request with invalid instance count."""
        with pytest.raises(ValidationError):
            SubmitJobRequest(
                job_name="test-job",
                job_config={},
                instance_count=0,  # Should be >= 1
                resource_type="CPU",
            )

    @pytest.mark.unit
    def test_submit_job_request_priority_bounds(self) -> None:
        """Test submit job request priority boundaries."""
        # Valid priorities
        SubmitJobRequest(
            job_name="test",
            job_config={},
            instance_count=1,
            resource_type="CPU",
            priority=-100,
        )
        SubmitJobRequest(
            job_name="test",
            job_config={},
            instance_count=1,
            resource_type="CPU",
            priority=100,
        )

        # Invalid priorities
        with pytest.raises(ValidationError):
            SubmitJobRequest(
                job_name="test",
                job_config={},
                instance_count=1,
                resource_type="CPU",
                priority=-101,
            )

    @pytest.mark.unit
    def test_get_job_status_request_valid(self) -> None:
        """Test valid get job status request."""
        request = GetJobStatusRequest(job_id="job-123")
        assert request.job_id == "job-123"

    @pytest.mark.unit
    def test_list_jobs_request_defaults(self) -> None:
        """Test list jobs request with defaults."""
        request = ListJobsRequest()
        assert request.limit == 10
        assert request.offset == 0
        assert request.status_filter is None

    @pytest.mark.unit
    def test_list_jobs_request_limit_bounds(self) -> None:
        """Test list jobs request limit boundaries."""
        # Valid limits
        ListJobsRequest(limit=1)
        ListJobsRequest(limit=100)

        # Invalid limits
        with pytest.raises(ValidationError):
            ListJobsRequest(limit=0)
        with pytest.raises(ValidationError):
            ListJobsRequest(limit=101)

    @pytest.mark.unit
    def test_cancel_job_request_optional_reason(self) -> None:
        """Test cancel job request with optional reason."""
        request1 = CancelJobRequest(job_id="job-123")
        assert request1.reason is None

        request2 = CancelJobRequest(job_id="job-123", reason="Test cancellation")
        assert request2.reason == "Test cancellation"


class TestOutputSchemas:
    """Test suite for output schemas."""

    @pytest.mark.unit
    def test_job_submitted_valid(self) -> None:
        """Test valid job submitted output."""
        now = datetime.utcnow()
        output = JobSubmitted(
            job_id="job-123",
            status="submitted",
            name="test-job",
            created_at=now,
            instance_count=4,
            resource_type="CPU",
        )

        assert output.job_id == "job-123"
        assert output.status == "submitted"

    @pytest.mark.unit
    def test_job_status_valid(self) -> None:
        """Test valid job status output."""
        now = datetime.utcnow()
        output = JobStatus(
            job_id="job-123",
            status="running",
            progress=50.0,
            started_at=now,
            updated_at=now,
            error_message=None,
        )

        assert output.job_id == "job-123"
        assert output.progress == 50.0

    @pytest.mark.unit
    def test_job_status_invalid_progress(self) -> None:
        """Test job status with invalid progress."""
        now = datetime.utcnow()

        with pytest.raises(ValidationError):
            JobStatus(
                job_id="job-123",
                status="running",
                progress=150.0,  # Should be <= 100
                started_at=now,
                updated_at=now,
            )

    @pytest.mark.unit
    def test_job_results_valid(self) -> None:
        """Test valid job results output."""
        output = JobResults(
            job_id="job-123",
            status="completed",
            results_url="https://storage.qarnot.com/results/job-123",
            file_size_bytes=1048576,
            file_count=5,
            download_url="https://storage.qarnot.com/download/xyz",
        )

        assert output.job_id == "job-123"
        assert output.file_count == 5

    @pytest.mark.unit
    def test_jobs_list_valid(self) -> None:
        """Test valid jobs list output."""
        now = datetime.utcnow()
        summaries = [
            JobSummary(
                job_id="job-1",
                status="running",
                name="job-1",
                created_at=now,
            ),
            JobSummary(
                job_id="job-2",
                status="completed",
                name="job-2",
                created_at=now,
            ),
        ]

        output = JobsList(
            total_count=10,
            jobs=summaries,
            next_offset=10,
        )

        assert output.total_count == 10
        assert len(output.jobs) == 2
        assert output.next_offset == 10
