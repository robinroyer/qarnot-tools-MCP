"""Cancel job use case.

This module implements the business logic for cancelling jobs.
"""

import logging
from typing import Optional

from src.domain.entities.job import Job
from src.ports.qarnot_port import QarnotPort

logger = logging.getLogger(__name__)


class CancelJobUseCase:
    """Use case for cancelling a running job.

    This encapsulates the business logic for job cancellation,
    independent of infrastructure concerns.
    """

    def __init__(self, qarnot_client: QarnotPort):
        """Initialize the use case.

        Args:
            qarnot_client: Port for interacting with Qarnot API
        """
        self.qarnot_client = qarnot_client

    async def execute(self, job_id: str, reason: Optional[str] = None) -> Job:
        """Execute the cancel job use case.

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
        logger.info(
            "Executing cancel job use case", extra={"job_id": job_id, "reason": reason}
        )

        job = await self.qarnot_client.cancel_job(job_id, reason)

        logger.info(
            "Job cancelled successfully", extra={"job_id": job_id, "status": job.status}
        )

        return job
