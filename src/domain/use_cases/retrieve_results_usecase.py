"""Retrieve job results use case.

This module implements the business logic for retrieving job results.
"""

import logging
from typing import Optional

from src.domain.entities.job_result import JobResult
from src.ports.qarnot_port import QarnotPort

logger = logging.getLogger(__name__)


class RetrieveResultsUseCase:
    """Use case for retrieving results from a completed job.

    This encapsulates the business logic for results retrieval,
    independent of infrastructure concerns.
    """

    def __init__(self, qarnot_client: QarnotPort):
        """Initialize the use case.

        Args:
            qarnot_client: Port for interacting with Qarnot API
        """
        self.qarnot_client = qarnot_client

    async def execute(
        self, job_id: str, output_path: Optional[str] = None
    ) -> JobResult:
        """Execute the retrieve results use case.

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
            "Executing retrieve results use case",
            extra={"job_id": job_id, "output_path": output_path}
        )

        result = await self.qarnot_client.retrieve_results(job_id, output_path)

        logger.info(
            "Results retrieved successfully",
            extra={
                "job_id": job_id,
                "file_count": result.file_count,
                "file_size_bytes": result.file_size_bytes,
            }
        )

        return result
