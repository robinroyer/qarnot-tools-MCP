"""Qarnot port (interface) for hexagonal architecture.

This module defines the abstract interface for Qarnot Computing operations.
Concrete implementations will wrap the Qarnot SDK.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from src.domain.entities.job import Job
from src.domain.entities.job_result import JobResult


class QarnotPort(ABC):
    """Abstract interface for Qarnot Computing operations.

    This port defines the contract for Qarnot adapters.
    Implementations must interact with the Qarnot API.
    """

    @abstractmethod
    async def submit_job(
        self,
        name: str,
        config: dict[str, Any],
        instance_count: int,
        resource_type: str,
        priority: int = 0,
        tags: Optional[list[str]] = None,
    ) -> Job:
        """Submit a new job to Qarnot Computing.

        Args:
            name: Human-readable name for the job
            config: Job configuration (script, docker image, etc.)
            instance_count: Number of compute instances to use
            resource_type: Type of resource ("GPU" or "CPU")
            priority: Job priority (-100 to 100)
            tags: Optional list of tags for filtering

        Returns:
            Job entity with created job information

        Raises:
            QarnotAPIError: If API call fails
            ValidationError: If parameters are invalid
        """
        pass

    @abstractmethod
    async def get_job_status(self, job_id: str) -> Job:
        """Get the current status of a job.

        Args:
            job_id: Unique identifier of the job

        Returns:
            Job entity with current status and progress

        Raises:
            QarnotAPIError: If API call fails
            JobNotFoundError: If job doesn't exist
        """
        pass

    @abstractmethod
    async def retrieve_results(
        self, job_id: str, output_path: Optional[str] = None
    ) -> JobResult:
        """Retrieve results from a completed job.

        Args:
            job_id: Unique identifier of the job
            output_path: Optional path to download results to

        Returns:
            JobResult entity with results metadata

        Raises:
            QarnotAPIError: If API call fails
            JobNotFoundError: If job doesn't exist
            JobNotCompletedError: If job hasn't completed yet
        """
        pass

    @abstractmethod
    async def cancel_job(self, job_id: str, reason: Optional[str] = None) -> Job:
        """Cancel a running job.

        Args:
            job_id: Unique identifier of the job
            reason: Optional reason for cancellation

        Returns:
            Job entity with cancelled status

        Raises:
            QarnotAPIError: If API call fails
            JobNotFoundError: If job doesn't exist
            JobAlreadyCompletedError: If job already completed
        """
        pass

    @abstractmethod
    async def list_jobs(
        self, limit: int = 10, offset: int = 0, status_filter: Optional[str] = None
    ) -> tuple[list[Job], int]:
        """List jobs for the authenticated user.

        Args:
            limit: Maximum number of jobs to return (1-100)
            offset: Number of jobs to skip for pagination
            status_filter: Optional status to filter by

        Returns:
            Tuple of (list of Job entities, total count)

        Raises:
            QarnotAPIError: If API call fails
        """
        pass
