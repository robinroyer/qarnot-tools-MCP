"""Get job status use case.

This module implements the business logic for retrieving job status.
"""

import logging

from src.domain.entities.job import Job
from src.ports.qarnot_port import QarnotPort

logger = logging.getLogger(__name__)


class GetJobStatusUseCase:
    """Use case for getting the status of a job.

    This encapsulates the business logic for status retrieval,
    independent of infrastructure concerns.
    """

    def __init__(self, qarnot_client: QarnotPort):
        """Initialize the use case.

        Args:
            qarnot_client: Port for interacting with Qarnot API
        """
        self.qarnot_client = qarnot_client

    async def execute(self, job_id: str) -> Job:
        """Execute the get job status use case.

        Args:
            job_id: Unique identifier of the job

        Returns:
            Job entity with current status and progress

        Raises:
            QarnotAPIError: If API call fails
            JobNotFoundError: If job doesn't exist
        """
        logger.info(
            "Executing get job status use case",
            extra={"job_id": job_id}
        )

        job = await self.qarnot_client.get_job_status(job_id)

        logger.info(
            "Job status retrieved",
            extra={
                "job_id": job_id,
                "status": job.status,
                "progress": job.progress,
            }
        )

        return job
