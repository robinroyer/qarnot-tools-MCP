"""Mock responses for Qarnot API tests.

This module provides mock data that simulates Qarnot API responses.
"""

from datetime import datetime, timedelta
from typing import Any

from src.domain.entities.job import Job
from src.domain.entities.job_result import JobResult


def create_mock_job(
    job_id: str = "job-mock-123",
    status: str = "running",
    progress: float = 50.0,
    **kwargs: Any,
) -> Job:
    """Create a mock job entity.

    Args:
        job_id: Job identifier
        status: Job status
        progress: Job progress percentage
        **kwargs: Additional job attributes

    Returns:
        Job entity with mock data
    """
    now = datetime.utcnow()
    defaults = {
        "job_id": job_id,
        "name": f"mock-job-{job_id}",
        "status": status,
        "instance_count": 4,
        "resource_type": "CPU",
        "priority": 0,
        "tags": ["mock", "test"],
        "config": {"docker_image": "python:3.11"},
        "created_at": now - timedelta(minutes=30),
        "started_at": now - timedelta(minutes=25) if status != "queued" else None,
        "updated_at": now,
        "completed_at": now if status in ["completed", "failed", "cancelled"] else None,
        "progress": progress,
        "error_message": "Mock error" if status == "failed" else None,
    }
    defaults.update(kwargs)
    return Job(**defaults)


def create_mock_job_result(
    job_id: str = "job-mock-123", status: str = "completed", **kwargs: Any
) -> JobResult:
    """Create a mock job result entity.

    Args:
        job_id: Job identifier
        status: Final job status
        **kwargs: Additional result attributes

    Returns:
        JobResult entity with mock data
    """
    defaults = {
        "job_id": job_id,
        "status": status,
        "results_url": f"https://storage.mock.qarnot.com/results/{job_id}",
        "file_size_bytes": 1048576,
        "file_count": 5,
        "download_url": f"https://storage.mock.qarnot.com/download/{job_id}",
        "checksum": "sha256:mock123abc",
    }
    defaults.update(kwargs)
    return JobResult(**defaults)


def create_mock_job_list(count: int = 3) -> list[Job]:
    """Create a list of mock jobs.

    Args:
        count: Number of jobs to create

    Returns:
        List of Job entities
    """
    statuses = ["queued", "running", "completed", "failed"]
    jobs = []

    for i in range(count):
        status = statuses[i % len(statuses)]
        progress = 100.0 if status in ["completed", "failed"] else float(i * 25)
        job = create_mock_job(
            job_id=f"job-mock-{i}",
            status=status,
            progress=progress,
        )
        jobs.append(job)

    return jobs
