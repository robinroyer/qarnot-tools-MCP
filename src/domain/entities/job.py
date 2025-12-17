"""Job entity for domain layer.

This module defines the Job entity which represents a computational job
in the Qarnot Computing platform.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class Job(BaseModel):
    """Domain entity representing a Qarnot job.

    This is the core domain model for jobs, independent of any
    infrastructure concerns.
    """

    job_id: str = Field(description="Unique identifier for the job")
    name: str = Field(description="Human-readable name of the job")
    status: str = Field(
        description="Current status of the job",
        pattern="^(submitted|queued|running|completed|failed|cancelled)$",
    )
    instance_count: int = Field(description="Number of compute instances", ge=1)
    resource_type: str = Field(
        description="Type of compute resource", pattern="^(GPU|CPU)$"
    )
    priority: int = Field(default=0, description="Job priority", ge=-100, le=100)
    tags: list[str] = Field(default_factory=list, description="Job tags")
    config: dict[str, Any] = Field(
        default_factory=dict,
        description="Job configuration (script, docker image, etc.)",
    )
    created_at: datetime = Field(description="Timestamp when job was created")
    started_at: Optional[datetime] = Field(
        default=None, description="Timestamp when job started execution"
    )
    updated_at: datetime = Field(description="Timestamp of last update")
    completed_at: Optional[datetime] = Field(
        default=None, description="Timestamp when job completed"
    )
    progress: float = Field(
        default=0.0, description="Job progress percentage", ge=0.0, le=100.0
    )
    error_message: Optional[str] = Field(
        default=None, description="Error message if job failed"
    )

    class Config:
        """Pydantic configuration."""

        frozen = True  # Make entity immutable
        json_schema_extra = {
            "example": {
                "job_id": "job-123abc",
                "name": "data-processing-job",
                "status": "running",
                "instance_count": 4,
                "resource_type": "CPU",
                "priority": 10,
                "tags": ["production", "data-pipeline"],
                "config": {"docker_image": "python:3.11"},
                "created_at": "2025-01-15T10:00:00Z",
                "started_at": "2025-01-15T10:05:00Z",
                "updated_at": "2025-01-15T10:30:00Z",
                "progress": 45.5,
            }
        }
