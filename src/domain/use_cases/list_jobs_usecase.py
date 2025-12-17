"""List jobs use case.

This module implements the business logic for listing jobs.
"""

import logging
from typing import Optional

from src.domain.entities.job import Job
from src.ports.qarnot_port import QarnotPort

logger = logging.getLogger(__name__)


class ListJobsUseCase:
    """Use case for listing user jobs.

    This encapsulates the business logic for job listing,
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
        limit: int = 10,
        offset: int = 0,
        status_filter: Optional[str] = None,
    ) -> tuple[list[Job], int, Optional[int]]:
        """Execute the list jobs use case.

        Args:
            limit: Maximum number of jobs to return (1-100)
            offset: Number of jobs to skip for pagination
            status_filter: Optional status to filter by

        Returns:
            Tuple of (list of Job entities, total count, next offset or None)

        Raises:
            QarnotAPIError: If API call fails
        """
        logger.info(
            "Executing list jobs use case",
            extra={
                "limit": limit,
                "offset": offset,
                "status_filter": status_filter,
            }
        )

        jobs, total_count = await self.qarnot_client.list_jobs(
            limit=limit,
            offset=offset,
            status_filter=status_filter,
        )

        # Calculate next offset for pagination
        next_offset = None
        if offset + len(jobs) < total_count:
            next_offset = offset + limit

        logger.info(
            "Jobs listed successfully",
            extra={
                "count": len(jobs),
                "total": total_count,
                "next_offset": next_offset,
            }
        )

        return jobs, total_count, next_offset
