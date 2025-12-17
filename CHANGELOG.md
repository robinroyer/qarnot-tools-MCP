# Changelog

All notable changes to the Qarnot MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial implementation of Qarnot MCP Server
- Hexagonal architecture with ports & adapters pattern
- 5 MCP tools: submit_job, get_job_status, retrieve_job_results, cancel_job, list_jobs
- Two-level authentication (Client→MCP, MCP→Qarnot)
- Comprehensive test suite (unit + integration tests)
- Docker support with multi-stage build
- Docker Compose configuration
- Health check endpoint
- Structured logging (JSON and text formats)
- Pydantic validation for all inputs/outputs
- Full type hints with mypy strict mode
- Code quality tools (Black, Ruff, mypy)
- CI/CD ready configuration
- Comprehensive documentation

### Security
- Bearer token authentication for MCP access
- API token authentication for Qarnot Cloud
- Timing-safe token comparison to prevent timing attacks
- Non-root Docker user
- Read-only filesystem in Docker
- No secrets in code or logs

## [1.0.0] - TBD

Initial release.
