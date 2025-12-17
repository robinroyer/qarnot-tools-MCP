# 🚀 Quick Start Guide

Get your Qarnot MCP Server running in 5 minutes!

## Prerequisites

- ✅ Python 3.11 or later
- ✅ Git (for cloning)
- ✅ Qarnot API account ([sign up here](https://account.qarnot.com))

## Option 1: Automated Quick Start (Recommended)

```bash
# Run the quick start script
./scripts/quickstart.sh
```

That's it! The script will:
1. Check your Python version
2. Create a virtual environment
3. Install all dependencies
4. Run tests to verify everything works
5. Start the MCP server

## Option 2: Manual Setup

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd mcp-server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
```

### Step 2: Configure

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your tokens
nano .env  # or vim, code, etc.
```

**Required configuration:**
```bash
MCP_AUTH_TOKEN=your_secure_mcp_token_here
QARNOT_API_TOKEN=your_qarnot_api_token_here
```

### Step 3: Verify Setup

```bash
# Run all tests
make test

# Or use pytest directly
pytest -v --cov=src
```

### Step 4: Start Server

```bash
# Using make
make run

# Or directly with Python
python -m src.main
```

Server will start at `http://localhost:3000`

## Option 3: Docker (Production-Ready)

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your tokens

# 2. Build and start
docker-compose up -d

# 3. Check logs
docker-compose logs -f mcp-server

# 4. Check health
curl http://localhost:3000/health
```

## 🧪 Testing Your Server

### 1. Health Check

```bash
curl http://localhost:3000/health
```

Expected response: `200 OK`

### 2. List Available Tools

```bash
curl -H "Authorization: Bearer YOUR_MCP_AUTH_TOKEN" \
     http://localhost:3000/tools
```

Should return 5 tools: `submit_job`, `get_job_status`, `retrieve_job_results`, `cancel_job`, `list_jobs`

### 3. Submit a Test Job

```bash
curl -X POST http://localhost:3000/tools/submit_job \
  -H "Authorization: Bearer YOUR_MCP_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "test-job",
    "job_config": {"docker_image": "python:3.11"},
    "instance_count": 1,
    "resource_type": "CPU"
  }'
```

## 🎯 Next Steps

### For Developers

1. **Explore the code:**
   ```bash
   # View project structure
   tree src/

   # Read the architecture docs
   cat PROJECT_SUMMARY.md
   ```

2. **Run quality checks:**
   ```bash
   make quality  # Runs format, lint, typecheck, tests
   ```

3. **Make changes and test:**
   ```bash
   # Format code
   make format

   # Run specific tests
   pytest tests/unit/test_auth_adapter.py -v
   ```

### For Users

1. **Configure your LLM client** (e.g., Claude) to use the MCP server:
   ```json
   {
     "mcpServers": {
       "qarnot": {
         "url": "http://localhost:3000",
         "auth": {
           "type": "bearer",
           "token": "YOUR_MCP_AUTH_TOKEN"
         }
       }
     }
   }
   ```

2. **Use the tools** through your LLM:
   - "Submit a job to process this data..."
   - "Check the status of job-abc123"
   - "List all my running jobs"

## 📊 Useful Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make test` | Run all tests with coverage |
| `make test-unit` | Run only unit tests |
| `make format` | Format code with Black |
| `make lint` | Check code quality |
| `make docker-build` | Build Docker image |
| `make docker-up` | Start Docker containers |
| `make docker-logs` | View Docker logs |
| `make clean` | Remove generated files |

## 🐛 Troubleshooting

### Server won't start

**Problem:** `ModuleNotFoundError` or import errors
```bash
# Solution: Reinstall dependencies
pip install -r requirements-dev.txt --force-reinstall
```

**Problem:** Port 3000 already in use
```bash
# Solution: Change port in .env
echo "MCP_PORT=3001" >> .env
```

### Authentication fails

**Problem:** `401 Unauthorized`
```bash
# Solution: Check your token
cat .env | grep MCP_AUTH_TOKEN

# Make sure it matches what you're sending in requests
curl -H "Authorization: Bearer $(grep MCP_AUTH_TOKEN .env | cut -d= -f2)" \
     http://localhost:3000/health
```

### Tests fail

**Problem:** Import errors in tests
```bash
# Solution: Install in development mode
pip install -e .
```

**Problem:** Coverage too low
```bash
# Solution: Check which files aren't covered
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## 🆘 Getting Help

- 📖 Read the full docs: `README.md`
- 🏗️ Understand architecture: `PROJECT_SUMMARY.md`
- 🐛 Report issues: GitHub Issues
- 💬 Questions: GitHub Discussions

## ✅ Verification Checklist

Before deploying to production:

- [ ] All tests pass (`make test`)
- [ ] Code quality checks pass (`make quality`)
- [ ] Environment variables are set
- [ ] Strong authentication tokens configured
- [ ] Health check responds correctly
- [ ] Docker container starts successfully
- [ ] Logs are configured (JSON format for production)
- [ ] Resource limits are set in docker-compose.yml
- [ ] Monitoring is configured (optional)

## 🎉 You're Ready!

Your Qarnot MCP Server is now running and ready to expose Qarnot Computing capabilities to LLMs!

**What's next?**
- Integrate with your LLM application
- Submit computational jobs via natural language
- Monitor job progress and retrieve results
- Scale your computational workloads with Qarnot

Happy computing! 🚀
