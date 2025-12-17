"""Output schemas for MCP tools.

This module defines Pydantic models for MCP tool responses.
All outputs are structured and validated before being returned.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class JobSubmitted(BaseModel):
    """Output schema for submit_job tool.

    Example:
        {
            "job_id": "job-abc123",
            "status": "submitted",
            "name": "data-processing-job",
            "created_at": "2025-01-15T10:00:00Z",
            "instance_count": 4,
            "resource_type": "CPU"
        }
    """

    job_id: str = Field(description="Unique identifier for the created job")
    status: str = Field(description="Initial status of the job")
    name: str = Field(description="Name of the job")
    created_at: datetime = Field(description="Timestamp when job was created")
    instance_count: int = Field(description="Number of compute instances")
    resource_type: str = Field(description="Type of compute resource")


class JobStatus(BaseModel):
    """Output schema for get_job_status tool.

    Example:
        {
            "job_id": "job-abc123",
            "status": "running",
            "progress": 45.5,
            "started_at": "2025-01-15T10:05:00Z",
            "updated_at": "2025-01-15T10:30:00Z",
            "error_message": null
        }
    """

    job_id: str = Field(description="Unique identifier of the job")
    status: str = Field(
        description="Current status",
        pattern="^(submitted|queued|running|completed|failed|cancelled)$",
    )
    progress: float = Field(description="Progress percentage (0-100)", ge=0.0, le=100.0)
    started_at: Optional[datetime] = Field(
        default=None, description="When job started execution"
    )
    updated_at: datetime = Field(description="Last update timestamp")
    error_message: Optional[str] = Field(
        default=None, description="Error message if job failed"
    )


class JobResults(BaseModel):
    """Output schema for retrieve_job_results tool.

    Example:
        {
            "job_id": "job-abc123",
            "status": "completed",
            "results_url": "https://storage.qarnot.com/results/job-abc123",
            "file_size_bytes": 1048576,
            "file_count": 5,
            "download_url": "https://storage.qarnot.com/download/xyz"
        }
    """

    job_id: str = Field(description="Unique identifier of the job")
    status: str = Field(description="Final status of the job")
    results_url: str = Field(description="URL to access results storage")
    file_size_bytes: int = Field(
        description="Total size of result files in bytes", ge=0
    )
    file_count: int = Field(description="Number of result files", ge=0)
    download_url: Optional[str] = Field(
        default=None, description="Pre-signed URL for direct download"
    )


class JobCancelled(BaseModel):
    """Output schema for cancel_job tool.

    Example:
        {
            "job_id": "job-abc123",
            "cancelled_at": "2025-01-15T11:00:00Z",
            "status": "cancelled",
            "reason": "User requested cancellation"
        }
    """

    job_id: str = Field(description="Unique identifier of the job")
    cancelled_at: datetime = Field(description="When job was cancelled")
    status: str = Field(description="Status after cancellation (should be 'cancelled')")
    reason: Optional[str] = Field(default=None, description="Reason for cancellation")


class JobSummary(BaseModel):
    """Summary information about a job for list_jobs.

    Example:
        {
            "job_id": "job-abc123",
            "status": "running",
            "name": "data-processing",
            "created_at": "2025-01-15T10:00:00Z"
        }
    """

    job_id: str = Field(description="Unique identifier of the job")
    status: str = Field(description="Current status")
    name: str = Field(description="Job name")
    created_at: datetime = Field(description="Creation timestamp")


class JobsList(BaseModel):
    """Output schema for list_jobs tool.

    Example:
        {
            "total_count": 45,
            "jobs": [...],
            "next_offset": 10
        }
    """

    total_count: int = Field(description="Total number of jobs matching filter", ge=0)
    jobs: list[JobSummary] = Field(description="List of jobs in this page")
    next_offset: Optional[int] = Field(
        default=None, description="Offset for next page (null if no more pages)"
    )
