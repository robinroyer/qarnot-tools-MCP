.PHONY: help install install-dev test test-unit test-integration coverage lint format typecheck clean docker-build docker-up docker-down docker-logs run

# Default target
help:
	@echo "Qarnot MCP Server - Available commands:"
	@echo ""
	@echo "  make install          - Install production dependencies"
	@echo "  make install-dev      - Install development dependencies"
	@echo "  make run              - Run the MCP server locally"
	@echo ""
	@echo "  make test             - Run all tests with coverage"
	@echo "  make test-unit        - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make coverage         - Generate HTML coverage report"
	@echo ""
	@echo "  make lint             - Run Ruff linter"
	@echo "  make format           - Format code with Black"
	@echo "  make typecheck        - Run mypy type checker"
	@echo "  make quality          - Run all quality checks"
	@echo ""
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-up        - Start Docker containers"
	@echo "  make docker-down      - Stop Docker containers"
	@echo "  make docker-logs      - View Docker logs"
	@echo ""
	@echo "  make clean            - Remove generated files"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

# Running
run:
	python -m src.main

# Testing
test:
	pytest -v --cov=src --cov-report=term-missing

test-unit:
	pytest -v -m unit --cov=src

test-integration:
	pytest -v -m integration --cov=src

coverage:
	pytest --cov=src --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Code quality
lint:
	ruff check src/ tests/

format:
	black src/ tests/

typecheck:
	mypy src/

quality: format lint typecheck test
	@echo "All quality checks passed!"

# Docker
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d
	@echo "MCP server started at http://localhost:3000"

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f mcp-server

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage 2>/dev/null || true
	@echo "Cleaned up generated files"
