"""Unit tests for Qarnot adapter.

Tests Qarnot SDK wrapper functionality and error handling.
"""

import pytest

from src.adapters.qarnot_adapter import QarnotAdapter
from src.config.settings import Settings
from src.domain.exceptions import (
    JobNotFoundError,
    QarnotAPIError,
)


class TestQarnotAdapter:
    """Test suite for QarnotAdapter."""

    @pytest.fixture
    def qarnot_adapter(self, test_settings: Settings) -> QarnotAdapter:
        """Provide QarnotAdapter instance.

        Args:
            test_settings: Test settings fixture

        Returns:
            QarnotAdapter instance
        """
        return QarnotAdapter(test_settings)

    @pytest.mark.unit
    @pytest.mark.qarnot
    async def test_submit_job_creates_job(
        self, qarnot_adapter: QarnotAdapter
    ) -> None:
        """Test that submit_job creates a job entity.

        Note: This test uses the mock implementation.
        In production, this would be tested with actual SDK.
        """
        job = await qarnot_adapter.submit_job(
            name="test-job",
            config={"docker_image": "python:3.11"},
            instance_count=4,
            resource_type="CPU",
            priority=10,
            tags=["test"],
        )

        assert job.name == "test-job"
        assert job.instance_count == 4
        assert job.resource_type == "CPU"
        assert job.status == "submitted"
        assert job.job_id.startswith("job-")

    @pytest.mark.unit
    @pytest.mark.qarnot
    async def test_get_job_status_not_found(
        self, qarnot_adapter: QarnotAdapter
    ) -> None:
        """Test getting status for non-existent job.

        Note: Mock implementation always raises JobNotFoundError.
        """
        with pytest.raises(JobNotFoundError) as exc_info:
            await qarnot_adapter.get_job_status("non-existent-job")

        assert "non-existent-job" in str(exc_info.value)

    @pytest.mark.unit
    @pytest.mark.qarnot
    async def test_list_jobs_returns_empty(
        self, qarnot_adapter: QarnotAdapter
    ) -> None:
        """Test listing jobs returns empty list.

        Note: Mock implementation returns empty list.
        """
        jobs, total = await qarnot_adapter.list_jobs(limit=10, offset=0)

        assert jobs == []
        assert total == 0

    @pytest.mark.unit
    @pytest.mark.qarnot
    async def test_adapter_initialization(
        self, test_settings: Settings
    ) -> None:
        """Test adapter initializes with correct settings."""
        adapter = QarnotAdapter(test_settings)

        assert adapter._api_url == test_settings.qarnot_api_url
        # Token should not be exposed in any way
        assert hasattr(adapter, "_api_token")
