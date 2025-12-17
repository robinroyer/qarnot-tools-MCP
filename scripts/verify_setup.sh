#!/bin/bash
# Verification script to check project completeness

set -e

echo "🔍 Qarnot MCP Server - Setup Verification"
echo "=========================================="
echo ""

ERRORS=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1"
    else
        echo "❌ $1 - MISSING"
        ERRORS=$((ERRORS + 1))
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo "✅ $1/"
    else
        echo "❌ $1/ - MISSING"
        ERRORS=$((ERRORS + 1))
    fi
}

echo "📁 Checking project structure..."
echo ""

# Core directories
check_dir "src"
check_dir "src/config"
check_dir "src/domain"
check_dir "src/domain/entities"
check_dir "src/domain/use_cases"
check_dir "src/ports"
check_dir "src/adapters"
check_dir "src/schemas"
check_dir "tests"
check_dir "tests/unit"
check_dir "tests/integration"
check_dir "tests/fixtures"
check_dir "docker"
check_dir "scripts"
echo ""

echo "📄 Checking core files..."
echo ""

# Configuration
check_file "src/config/settings.py"
check_file ".env.example"
check_file ".gitignore"

# Domain
check_file "src/domain/entities/job.py"
check_file "src/domain/entities/job_result.py"
check_file "src/domain/exceptions.py"

# Ports
check_file "src/ports/auth_port.py"
check_file "src/ports/qarnot_port.py"
check_file "src/ports/mcp_port.py"

# Adapters
check_file "src/adapters/auth_adapter.py"
check_file "src/adapters/qarnot_adapter.py"
check_file "src/adapters/mcp_adapter.py"

# Use cases
check_file "src/domain/use_cases/submit_job_usecase.py"
check_file "src/domain/use_cases/get_job_status_usecase.py"
check_file "src/domain/use_cases/retrieve_results_usecase.py"
check_file "src/domain/use_cases/cancel_job_usecase.py"
check_file "src/domain/use_cases/list_jobs_usecase.py"

# Schemas
check_file "src/schemas/inputs.py"
check_file "src/schemas/outputs.py"

# Main
check_file "src/main.py"
check_file "src/health.py"

echo ""
echo "🧪 Checking test files..."
echo ""

check_file "tests/conftest.py"
check_file "tests/unit/test_auth_adapter.py"
check_file "tests/unit/test_qarnot_adapter.py"
check_file "tests/unit/test_use_cases.py"
check_file "tests/unit/test_schemas.py"
check_file "tests/integration/test_mcp_server.py"
check_file "tests/fixtures/mock_qarnot_responses.py"

echo ""
echo "🐳 Checking Docker files..."
echo ""

check_file "docker/Dockerfile"
check_file "docker/.dockerignore"
check_file "docker-compose.yml"

echo ""
echo "📦 Checking configuration files..."
echo ""

check_file "requirements.txt"
check_file "requirements-dev.txt"
check_file "pytest.ini"
check_file "pyproject.toml"
check_file "Makefile"

echo ""
echo "📚 Checking documentation..."
echo ""

check_file "README.md"
check_file "CHANGELOG.md"
check_file "LICENSE"
check_file "PROJECT_SUMMARY.md"

echo ""
echo "🔧 Checking scripts..."
echo ""

check_file "scripts/quickstart.sh"
check_file "scripts/verify_setup.sh"

echo ""
echo "=========================================="
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✅ All checks passed! Project is complete."
    echo ""
    echo "Next steps:"
    echo "1. Copy .env.example to .env and configure your tokens"
    echo "2. Run 'make install-dev' to install dependencies"
    echo "3. Run 'make test' to verify everything works"
    echo "4. Run 'make run' to start the server"
    echo ""
    exit 0
else
    echo "❌ Found $ERRORS missing files/directories"
    echo "Please check the project structure."
    echo ""
    exit 1
fi
