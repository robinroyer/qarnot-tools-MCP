# Qarnot MCP Server

A Model Context Protocol (MCP) HTTP server that exposes [Qarnot Computing](https://qarnot.com) capabilities as tools for Large Language Models (LLMs) like Claude.

## Features

- **5 MCP Tools**: Submit jobs, check status, retrieve results, cancel jobs, and list jobs
- **Secure Authentication**: Two-level auth (Client→MCP, MCP→Qarnot)
- **Hexagonal Architecture**: Clean separation of concerns with ports & adapters
- **Type-Safe**: Full type hints with Pydantic validation
- **Well-Tested**: 80%+ test coverage with unit and integration tests
- **Production-Ready**: Docker support, structured logging, health checks

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     MCP Client (Claude, etc.)                │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP + Bearer Token
┌───────────────────────────▼─────────────────────────────────┐
│                      MCP Server (FastMCP)                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │               MCP Adapter (Presentation)               │ │
│  └────────────────────────┬───────────────────────────────┘ │
│  ┌────────────────────────▼───────────────────────────────┐ │
│  │          Use Cases (Application Logic)                 │ │
│  │  • SubmitJobUseCase    • GetStatusUseCase              │ │
│  │  • RetrieveResultsUseCase  • CancelJobUseCase          │ │
│  │  • ListJobsUseCase                                     │ │
│  └────────────────────────┬───────────────────────────────┘ │
│  ┌────────────────────────▼───────────────────────────────┐ │
│  │              Ports (Interfaces)                        │ │
│  │  • QarnotPort    • AuthPort                            │ │
│  └────────────────────────┬───────────────────────────────┘ │
│  ┌────────────────────────▼───────────────────────────────┐ │
│  │              Adapters (Infrastructure)                 │ │
│  │  • QarnotAdapter (SDK Wrapper)                         │ │
│  │  • BearerTokenAuth                                     │ │
│  └────────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                            │ Qarnot API Token
┌───────────────────────────▼─────────────────────────────────┐
│                   Qarnot Cloud API                           │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)
- Qarnot API account and token

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp-server
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements-dev.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your actual tokens
```

5. Run the server:
```bash
python -m src.main
```

### Docker Deployment

1. Configure environment:
```bash
cp .env.example .env
# Edit .env with your actual tokens
```

2. Build and run with Docker Compose:
```bash
docker-compose build
docker-compose up -d
```

3. Check health:
```bash
curl http://localhost:3000/health
```

## Configuration

All configuration is done via environment variables. See `.env.example` for details.

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MCP_AUTH_TOKEN` | Bearer token for MCP authentication | `mcp_secret_123abc` |
| `QARNOT_API_TOKEN` | Qarnot Cloud API token | `sk_live_your_token` |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_HOST` | `0.0.0.0` | Host to bind server |
| `MCP_PORT` | `3000` | Port to bind server |
| `QARNOT_API_URL` | `https://api.qarnot.com` | Qarnot API URL |
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOG_FORMAT` | `json` | Log format (`json` or `text`) |

## MCP Tools

### 1. submit_job

Submit a new computational job to Qarnot.

**Input:**
```json
{
  "job_name": "data-processing-2025",
  "job_config": {
    "docker_image": "python:3.11",
    "script": "process.py"
  },
  "instance_count": 4,
  "resource_type": "CPU",
  "priority": 10,
  "tags": ["production"]
}
```

**Output:**
```json
{
  "job_id": "job-abc123",
  "status": "submitted",
  "name": "data-processing-2025",
  "created_at": "2025-01-15T10:00:00Z",
  "instance_count": 4,
  "resource_type": "CPU"
}
```

### 2. get_job_status

Get the current status of a job.

**Input:**
```json
{
  "job_id": "job-abc123"
}
```

**Output:**
```json
{
  "job_id": "job-abc123",
  "status": "running",
  "progress": 45.5,
  "started_at": "2025-01-15T10:05:00Z",
  "updated_at": "2025-01-15T10:30:00Z",
  "error_message": null
}
```

### 3. retrieve_job_results

Retrieve results from a completed job.

**Input:**
```json
{
  "job_id": "job-abc123",
  "output_path": "/tmp/results"
}
```

**Output:**
```json
{
  "job_id": "job-abc123",
  "status": "completed",
  "results_url": "https://storage.qarnot.com/results/job-abc123",
  "file_size_bytes": 1048576,
  "file_count": 5,
  "download_url": "https://storage.qarnot.com/download/xyz"
}
```

### 4. cancel_job

Cancel a running job.

**Input:**
```json
{
  "job_id": "job-abc123",
  "reason": "No longer needed"
}
```

**Output:**
```json
{
  "job_id": "job-abc123",
  "cancelled_at": "2025-01-15T11:00:00Z",
  "status": "cancelled",
  "reason": "No longer needed"
}
```

### 5. list_jobs

List jobs with pagination and filtering.

**Input:**
```json
{
  "limit": 20,
  "offset": 0,
  "status_filter": "running"
}
```

**Output:**
```json
{
  "total_count": 45,
  "jobs": [
    {
      "job_id": "job-abc123",
      "status": "running",
      "name": "data-processing",
      "created_at": "2025-01-15T10:00:00Z"
    }
  ],
  "next_offset": 20
}
```

## Authentication

### Level 1: Client → MCP Server

Clients must include a Bearer token in requests:

```bash
curl -H "Authorization: Bearer mcp_secret_123abc" \
     http://localhost:3000/tools
```

### Level 2: MCP Server → Qarnot Cloud

The MCP server authenticates to Qarnot using the API token from `QARNOT_API_TOKEN`.

**Security Notes:**
- Never commit tokens to version control
- Use strong, unique tokens in production
- Rotate tokens regularly
- Use HTTPS in production

## Development

### Running Tests

```bash
# Run all tests with coverage
pytest -v --cov

# Run unit tests only
pytest -v -m unit

# Run integration tests only
pytest -v -m integration

# Run specific test file
pytest tests/unit/test_auth_adapter.py -v
```

### Code Quality

```bash
# Format code with Black
black src/ tests/

# Lint with Ruff
ruff check src/ tests/

# Type check with mypy
mypy src/
```

### Project Structure

```
mcp-server/
├── src/
│   ├── config/          # Configuration and settings
│   ├── domain/          # Business logic and entities
│   │   ├── entities/    # Domain models (Job, JobResult)
│   │   ├── use_cases/   # Application logic
│   │   └── exceptions.py
│   ├── ports/           # Abstract interfaces
│   ├── adapters/        # Infrastructure implementations
│   ├── schemas/         # Pydantic validation schemas
│   └── main.py          # Application entry point
├── tests/
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   ├── fixtures/        # Test fixtures and mocks
│   └── conftest.py      # Pytest configuration
├── docker/
│   ├── Dockerfile       # Multi-stage Docker build
│   └── .dockerignore
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Development dependencies
├── pytest.ini           # Pytest configuration
├── pyproject.toml       # Tool configuration
├── docker-compose.yml   # Docker Compose setup
└── README.md            # This file
```

## Troubleshooting

### Server won't start

1. Check environment variables are set:
```bash
python -c "from src.config.settings import Settings; print(Settings())"
```

2. Check port is available:
```bash
lsof -i :3000  # On Linux/Mac
netstat -ano | findstr :3000  # On Windows
```

### Authentication errors

- Verify `MCP_AUTH_TOKEN` matches between client and server
- Ensure Bearer token is included in Authorization header
- Check `QARNOT_API_TOKEN` is valid and has correct permissions

### Qarnot API errors

- Verify `QARNOT_API_TOKEN` is valid
- Check `QARNOT_API_URL` is correct
- Review logs for detailed error messages

### Docker issues

```bash
# View logs
docker-compose logs -f mcp-server

# Restart container
docker-compose restart mcp-server

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and quality checks
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Follow hexagonal architecture principles
- Write tests for all new features (maintain 80%+ coverage)
- Use type hints for all functions
- Format code with Black
- Pass Ruff linting
- Pass mypy type checking
- Update documentation

## License

[Your License Here]

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review Qarnot documentation: https://docs.qarnot.com

## Acknowledgments

- Built with [FastMCP](https://github.com/modelcontextprotocol/python-sdk)
- Powered by [Qarnot Computing](https://qarnot.com)
- Inspired by [Model Context Protocol](https://modelcontextprotocol.io)
