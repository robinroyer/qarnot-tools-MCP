"""Submit job use case.

This module implements the business logic for submitting jobs to Qarnot.
"""

import logging
from typing import Any, Optional

from src.domain.entities.job import Job
from src.ports.qarnot_port import QarnotPort

logger = logging.getLogger(__name__)


class SubmitJobUseCase:
    """Use case for submitting a new job to Qarnot Computing.

    This encapsulates the business logic for job submission,
    independent of infrastructure concerns.
    """

    def __init__(self, qarnot_client: QarnotPort):
        """Initialize the use case.

        Args:
            qarnot_client: Port for interacting with Qarnot API
        """
        self.qarnot_client = qarnot_client

    async def execute(
        self,
        name: str,
        config: dict[str, Any],
        instance_count: int,
        resource_type: str,
        priority: int = 0,
        tags: Optional[list[str]] = None,
    ) -> Job:
        """Execute the submit job use case.

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
        logger.info(
            "Executing submit job use case",
            extra={
                "name": name,
                "instance_count": instance_count,
                "resource_type": resource_type,
            }
        )

        # Business logic could include additional validation,
        # pre-processing, or orchestration here

        job = await self.qarnot_client.submit_job(
            name=name,
            config=config,
            instance_count=instance_count,
            resource_type=resource_type,
            priority=priority,
            tags=tags,
        )

        logger.info(
            "Job submitted successfully",
            extra={"job_id": job.job_id, "name": name}
        )

        return job
