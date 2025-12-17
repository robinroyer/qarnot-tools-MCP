"""Input schemas for MCP tools.

This module defines Pydantic models for validating inputs to MCP tools.
All inputs are validated before being passed to use cases.
"""

from typing import Any, Optional

from pydantic import BaseModel, Field


class SubmitJobRequest(BaseModel):
    """Input schema for submitting a new job.

    Example:
        {
            "job_name": "data-processing-2025",
            "job_config": {"docker_image": "python:3.11", "script": "process.py"},
            "instance_count": 4,
            "resource_type": "CPU",
            "priority": 10,
            "tags": ["production", "data-pipeline"]
        }
    """

    job_name: str = Field(
        description="Unique name for the job",
        min_length=1,
        max_length=100,
        examples=["data-processing-job", "ml-training-2025"]
    )
    job_config: dict[str, Any] = Field(
        description="Job configuration (script, docker image, environment, etc.)",
        examples=[
            {
                "docker_image": "python:3.11",
                "script": "process_data.py",
                "environment": {"DATA_SOURCE": "s3://bucket/data"}
            }
        ]
    )
    instance_count: int = Field(
        description="Number of compute instances to use",
        ge=1,
        le=10000,
        examples=[1, 4, 16]
    )
    resource_type: str = Field(
        description="Type of compute resource",
        pattern="^(GPU|CPU)$",
        examples=["CPU", "GPU"]
    )
    priority: int = Field(
        default=0,
        description="Job priority (-100 to 100, higher is more important)",
        ge=-100,
        le=100,
        examples=[0, 10, -50]
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Tags for organizing and filtering jobs",
        examples=[["production"], ["dev", "testing"]]
    )


class GetJobStatusRequest(BaseModel):
    """Input schema for getting job status.

    Example:
        {
            "job_id": "job-abc123def456"
        }
    """

    job_id: str = Field(
        description="Unique identifier of the job",
        min_length=1,
        examples=["job-abc123", "12345-abcde"]
    )


class RetrieveResultsRequest(BaseModel):
    """Input schema for retrieving job results.

    Example:
        {
            "job_id": "job-abc123def456",
            "output_path": "/path/to/download"
        }
    """

    job_id: str = Field(
        description="Unique identifier of the job",
        min_length=1,
        examples=["job-abc123"]
    )
    output_path: Optional[str] = Field(
        default=None,
        description="Optional local path to download results to",
        examples=["/tmp/results", "./output"]
    )


class CancelJobRequest(BaseModel):
    """Input schema for cancelling a job.

    Example:
        {
            "job_id": "job-abc123def456",
            "reason": "User requested cancellation"
        }
    """

    job_id: str = Field(
        description="Unique identifier of the job to cancel",
        min_length=1,
        examples=["job-abc123"]
    )
    reason: Optional[str] = Field(
        default=None,
        description="Reason for cancellation (optional)",
        max_length=500,
        examples=["No longer needed", "Incorrect configuration"]
    )


class ListJobsRequest(BaseModel):
    """Input schema for listing jobs.

    Example:
        {
            "limit": 20,
            "offset": 0,
            "status_filter": "running"
        }
    """

    limit: int = Field(
        default=10,
        description="Maximum number of jobs to return",
        ge=1,
        le=100,
        examples=[10, 25, 100]
    )
    offset: int = Field(
        default=0,
        description="Number of jobs to skip (for pagination)",
        ge=0,
        examples=[0, 10, 20]
    )
    status_filter: Optional[str] = Field(
        default=None,
        description="Filter jobs by status",
        pattern="^(queued|running|completed|failed|cancelled)$",
        examples=["running", "completed", None]
    )
