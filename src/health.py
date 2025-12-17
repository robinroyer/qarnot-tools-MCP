"""Health check endpoint for the MCP server.

This module provides a simple health check that can be used by
Docker healthchecks, load balancers, and monitoring systems.
"""

import http.client
import sys


def check_health(host: str = "localhost", port: int = 3000) -> bool:
    """Check if the MCP server is healthy.

    Args:
        host: Server host
        port: Server port

    Returns:
        True if server is healthy, False otherwise
    """
    try:
        conn = http.client.HTTPConnection(host, port, timeout=5)
        conn.request("GET", "/health")
        response = conn.getresponse()
        conn.close()
        return response.status == 200
    except Exception:
        return False


if __name__ == "__main__":
    """Run health check from command line."""
    is_healthy = check_health()
    sys.exit(0 if is_healthy else 1)
