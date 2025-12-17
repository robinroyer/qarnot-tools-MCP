"""Job result entity for domain layer.

This module defines the JobResult entity which represents the output
and results of a completed job.
"""

from typing import Optional

from pydantic import BaseModel, Field


class JobResult(BaseModel):
    """Domain entity representing job execution results.

    Contains metadata and access information for job output files
    and artifacts.
    """

    job_id: str = Field(description="ID of the job these results belong to")
    status: str = Field(
        description="Final status of the job", pattern="^(completed|failed|cancelled)$"
    )
    results_url: str = Field(description="URL to access results storage")
    file_size_bytes: int = Field(
        description="Total size of result files in bytes", ge=0
    )
    file_count: int = Field(description="Number of result files", ge=0)
    download_url: Optional[str] = Field(
        default=None, description="Pre-signed URL for direct download (if available)"
    )
    checksum: Optional[str] = Field(
        default=None, description="Checksum of results archive (if applicable)"
    )

    class Config:
        """Pydantic configuration."""

        frozen = True  # Make entity immutable
        json_schema_extra = {
            "example": {
                "job_id": "job-123abc",
                "status": "completed",
                "results_url": "https://storage.qarnot.com/results/job-123abc",
                "file_size_bytes": 1048576,
                "file_count": 5,
                "download_url": "https://storage.qarnot.com/download/xyz",
                "checksum": "sha256:abc123def456",
            }
        }
