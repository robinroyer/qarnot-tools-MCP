#!/bin/bash
# Quick start script for Qarnot MCP Server

set -e

echo "🚀 Qarnot MCP Server - Quick Start"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or later."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
if (( $(echo "$PYTHON_VERSION < 3.11" | bc -l) )); then
    echo "❌ Python 3.11 or later is required. Current version: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your tokens:"
    echo "   - MCP_AUTH_TOKEN: Your MCP server authentication token"
    echo "   - QARNOT_API_TOKEN: Your Qarnot API token"
    echo ""
    echo "Press Enter when ready..."
    read -r
fi

# Create virtual environment if it doesn't exist
if [ ! -d venv ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements-dev.txt
echo "✅ Dependencies installed"
echo ""

# Run tests
echo "🧪 Running tests..."
pytest -v --cov=src --cov-report=term-missing
echo ""

# Check code quality
echo "🔍 Checking code quality..."
echo "  - Running Black..."
black --check src/ tests/ || echo "⚠️  Code formatting issues found (run 'black src/ tests/' to fix)"

echo "  - Running Ruff..."
ruff check src/ tests/ || echo "⚠️  Linting issues found"

echo "  - Running mypy..."
mypy src/ || echo "⚠️  Type checking issues found"
echo ""

# Start server
echo "🎉 Setup complete! Starting MCP server..."
echo ""
echo "Server will be available at http://localhost:3000"
echo "Press Ctrl+C to stop the server"
echo ""

python -m src.main
