"""Qarnot adapter implementation.

This module wraps the Qarnot SDK to implement the QarnotPort interface.
It handles all interactions with the Qarnot Computing API.
"""

import logging
from datetime import datetime
from typing import Any, Optional

from src.config.settings import Settings
from src.domain.entities.job import Job
from src.domain.entities.job_result import JobResult
from src.domain.exceptions import (
    JobAlreadyCompletedError,
    JobNotCompletedError,
    JobNotFoundError,
    QarnotAPIError,
    QarnotConnectionError,
    QarnotTimeoutError,
)
from src.ports.qarnot_port import QarnotPort

logger = logging.getLogger(__name__)


class QarnotAdapter(QarnotPort):
    """Qarnot SDK wrapper implementing QarnotPort.

    This adapter translates between our domain models and the Qarnot SDK.
    It handles error translation and logging.

    Note: The actual Qarnot SDK integration would use the 'qarnot' package.
    This implementation provides the structure and error handling patterns.
    """

    def __init__(self, settings: Settings):
        """Initialize the Qarnot adapter.

        Args:
            settings: Application settings with Qarnot API credentials

        Note:
            In production, this would initialize:
            self.client = qarnot.Client(
                auth_token=settings.qarnot_api_token,
                api_url=settings.qarnot_api_url
            )
        """
        self._api_token = settings.qarnot_api_token
        self._api_url = settings.qarnot_api_url

        # In production: Initialize actual Qarnot client
        # from qarnot import Client
        # self.client = Client(
        #     auth_token=self._api_token,
        #     api_url=self._api_url
        # )

        logger.info("Qarnot adapter initialized", extra={"api_url": self._api_url})

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
            QarnotConnectionError: If connection fails
            QarnotTimeoutError: If request times out
        """
        logger.info(
            "Submitting job",
            extra={
                "name": name,
                "instance_count": instance_count,
                "resource_type": resource_type,
                "priority": priority,
            },
        )

        try:
            # Production implementation would use Qarnot SDK:
            # task = self.client.create_task(name=name, profile="docker-batch")
            # task.constants = config
            # task.instance_count = instance_count
            # task.submit()

            # Mock implementation for structure demonstration
            now = datetime.utcnow()
            job_id = f"job-{name}-{now.timestamp()}"

            job = Job(
                job_id=job_id,
                name=name,
                status="submitted",
                instance_count=instance_count,
                resource_type=resource_type,
                priority=priority,
                tags=tags or [],
                config=config,
                created_at=now,
                updated_at=now,
                progress=0.0,
            )

            logger.info(
                "Job submitted successfully", extra={"job_id": job_id, "name": name}
            )

            return job

        except ConnectionError as e:
            logger.error(
                "Connection error while submitting job",
                extra={"name": name},
                exc_info=e,
            )
            raise QarnotConnectionError(f"Failed to connect to Qarnot API: {e}")

        except TimeoutError as e:
            logger.error(
                "Timeout while submitting job", extra={"name": name}, exc_info=e
            )
            raise QarnotTimeoutError(f"Request timed out: {e}")

        except Exception as e:
            logger.error(
                "Unexpected error submitting job", extra={"name": name}, exc_info=e
            )
            raise QarnotAPIError(f"Failed to submit job: {e}")

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
        logger.info("Getting job status", extra={"job_id": job_id})

        try:
            # Production implementation would use Qarnot SDK:
            # task = self.client.retrieve_task(job_id)
            # return self._map_task_to_job(task)

            # Mock implementation
            # In production, this would actually fetch from Qarnot API
            raise JobNotFoundError(job_id)

        except JobNotFoundError:
            raise

        except Exception as e:
            logger.error(
                "Error getting job status", extra={"job_id": job_id}, exc_info=e
            )
            raise QarnotAPIError(f"Failed to get job status: {e}")

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
        logger.info(
            "Retrieving job results",
            extra={"job_id": job_id, "output_path": output_path},
        )

        try:
            # Production implementation would:
            # 1. Get job status to check if completed
            # 2. Download results if output_path provided
            # 3. Return JobResult with metadata

            # Mock check for job completion
            job = await self.get_job_status(job_id)

            if job.status not in ["completed", "failed", "cancelled"]:
                raise JobNotCompletedError(job_id, job.status)

            # Mock result
            result = JobResult(
                job_id=job_id,
                status=job.status,
                results_url=f"https://storage.qarnot.com/results/{job_id}",
                file_size_bytes=1048576,
                file_count=5,
                download_url=f"https://storage.qarnot.com/download/{job_id}",
            )

            logger.info(
                "Results retrieved successfully",
                extra={
                    "job_id": job_id,
                    "file_count": result.file_count,
                    "file_size_bytes": result.file_size_bytes,
                },
            )

            return result

        except (JobNotFoundError, JobNotCompletedError):
            raise

        except Exception as e:
            logger.error(
                "Error retrieving results", extra={"job_id": job_id}, exc_info=e
            )
            raise QarnotAPIError(f"Failed to retrieve results: {e}")

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
        logger.info("Cancelling job", extra={"job_id": job_id, "reason": reason})

        try:
            # Production implementation would:
            # 1. Get current job status
            # 2. Check if cancellable
            # 3. Cancel via SDK
            # 4. Return updated job

            job = await self.get_job_status(job_id)

            if job.status in ["completed", "failed", "cancelled"]:
                raise JobAlreadyCompletedError(job_id, job.status)

            # Mock cancellation
            # In production: self.client.abort_task(job_id)

            logger.info(
                "Job cancelled successfully", extra={"job_id": job_id, "reason": reason}
            )

            # Return job would be updated with cancelled status
            return job

        except (JobNotFoundError, JobAlreadyCompletedError):
            raise

        except Exception as e:
            logger.error("Error cancelling job", extra={"job_id": job_id}, exc_info=e)
            raise QarnotAPIError(f"Failed to cancel job: {e}")

    async def list_jobs(
        self,
        limit: int = 10,
        offset: int = 0,
        status_filter: Optional[str] = None,
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
        logger.info(
            "Listing jobs",
            extra={
                "limit": limit,
                "offset": offset,
                "status_filter": status_filter,
            },
        )

        try:
            # Production implementation would use Qarnot SDK:
            # tasks = self.client.tasks()
            # Apply filtering and pagination
            # Map to Job entities

            # Mock implementation
            jobs: list[Job] = []
            total_count = 0

            logger.info(
                "Jobs listed successfully",
                extra={"count": len(jobs), "total": total_count},
            )

            return jobs, total_count

        except Exception as e:
            logger.error(
                "Error listing jobs",
                extra={"limit": limit, "offset": offset},
                exc_info=e,
            )
            raise QarnotAPIError(f"Failed to list jobs: {e}")
