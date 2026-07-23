# Local Development & Testing Guide

This guide shows how to run tests and CI checks locally before pushing to GitHub.

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- MySQL 8.0
- Git

### Setup

```bash
# 1. Clone repository
git clone https://github.com/ayaan9618/thinkloop_ai.git
cd thinkloop_ai

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env

# 5. Start MySQL (using Docker)
docker run -d \
  --name thinkloop-mysql \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=thinkloop_ai \
  -p 3306:3306 \
  mysql:8.0

# 6. Run tests
pytest backend/tests/ -v
```

## 📊 Running Tests

### All tests
```bash
pytest backend/tests/ -v
```

### Specific test file
```bash
pytest backend/tests/test_health.py -v
```

### Specific test function
```bash
pytest backend/tests/test_health.py::TestHealthCheck::test_health_check_success -v
```

### With coverage report
```bash
pytest backend/tests/ \
  --cov=backend \
  --cov-report=html \
  --cov-report=term-missing
```

### Only unit tests (skip slow tests)
```bash
pytest backend/tests/ -m unit
```

### With detailed output
```bash
pytest backend/tests/ -vv --tb=long
```

## 🔍 Code Quality Checks

### Format code with Black
```bash
black backend/ --line-length=100
```

### Check formatting without modifying
```bash
black backend/ --check --line-length=100
```

### Lint with Flake8
```bash
flake8 backend/ --max-line-length=100 --exclude=__pycache__,migrations
```

### Type check with MyPy
```bash
mypy backend/ --ignore-missing-imports --no-implicit-optional
```

### Security scan with Bandit
```bash
bandit -r backend/ -f txt
```

### All checks at once
```bash
black backend/ --check
flake8 backend/
mypy backend/
bandit -r backend/
pytest backend/tests/ --cov=backend
```

## 🐳 Using Docker Compose

### Start all services
```bash
docker-compose up -d
```

Services:
- MySQL (port 3306)
- Redis (port 6379)
- FastAPI (port 8000)
- Frontend (port 3000, optional)

### View logs
```bash
docker-compose logs -f backend
```

### Stop services
```bash
docker-compose down
```

### Remove volumes (reset database)
```bash
docker-compose down -v
```

## 🧪 Before Committing

Run this checklist before pushing:

```bash
# 1. Format code
black backend/

# 2. Sort imports
isort backend/ --profile black --line-length=100

# 3. Lint
flake8 backend/

# 4. Type check
mypy backend/

# 5. Security scan
bandit -r backend/

# 6. Run tests with coverage
pytest backend/tests/ \
  --cov=backend \
  --cov-report=term-missing \
  --cov-fail-under=80

# 7. Build check
python -m build 2>/dev/null || echo "Build check skipped"
```

Or use the convenience script:

```bash
# Create script: scripts/precommit.sh
#!/bin/bash
set -e
echo "Running pre-commit checks..."
black backend/
isort backend/ --profile black
flake8 backend/
mypy backend/
bandit -r backend/
pytest backend/tests/ --cov=backend --cov-fail-under=80
echo "✅ All checks passed!"

# Make executable
chmod +x scripts/precommit.sh

# Run before committing
./scripts/precommit.sh
```

## 🔄 Git Workflow

### Create feature branch
```bash
git checkout -b feature/new-feature
```

### Make changes
```bash
# Edit files...

# Run pre-commit checks
./scripts/precommit.sh  # or run all checks manually

# Stage changes
git add backend/

# Commit with conventional message
git commit -m "feat: add new feature"
```

### Push to GitHub
```bash
git push origin feature/new-feature
```

This triggers GitHub Actions CI pipeline which will:
- ✅ Run all tests
- ✅ Check code quality
- ✅ Run security scan
- ✅ Generate coverage report
- ✅ Comment on PR with results

### Create Pull Request
- Go to GitHub
- Click "Compare & pull request"
- Fill out PR template
- Request reviewers
- Wait for CI to pass
- Address review comments
- Merge when approved

## 🐛 Debugging

### Run specific test with verbose output
```bash
pytest backend/tests/test_file.py::test_function -vv --tb=long
```

### Drop into debugger
```python
# In your code
import pdb; pdb.set_trace()

# Then run test
pytest backend/tests/test_file.py -s  # -s shows print output
```

### Run with logging
```bash
pytest backend/tests/ -s --log-cli-level=DEBUG
```

### Generate report for CI failure
```bash
pytest backend/tests/ \
  --html=report.html \
  --self-contained-html \
  --cov=backend \
  --cov-report=html
```

## 📝 Common Issues

### Import errors
```bash
# Ensure project root is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or run with python module
python -m pytest backend/tests/
```

### MySQL connection failed
```bash
# Check MySQL is running
docker ps | grep mysql

# Or start Docker container
docker run -d \
  --name thinkloop-mysql \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=thinkloop_ai \
  -p 3306:3306 \
  mysql:8.0
```

### Tests timeout
```bash
# Run with longer timeout
pytest backend/tests/ --timeout=300
```

### Clear cache
```bash
# Remove cache files
rm -rf .pytest_cache __pycache__ .mypy_cache

# Clear pip cache
pip cache purge
```

## 📊 Coverage Goals

- **Minimum**: 80% code coverage
- **Target**: 90%+ code coverage
- **Critical paths**: 100% coverage

View coverage report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## 🚀 Performance Testing

### Profile code
```bash
python -m cProfile -s cumulative backend/app/main.py
```

### Load testing
```bash
# Install locust
pip install locust

# Create locustfile.py with tests
# Run load test
locust -f locustfile.py -u 100 -r 10
```

## 📚 Useful Commands

```bash
# Check Python version
python --version

# List installed packages
pip list

# Update all packages
pip install --upgrade -r requirements.txt

# Create requirements from current environment
pip freeze > requirements-all.txt

# Run type checking in strict mode
mypy backend/ --strict

# Run tests in parallel
pytest backend/tests/ -n auto

# Run tests and update snapshots
pytest backend/tests/ --snapshot-update

# Generate test report
pytest backend/tests/ --junitxml=report.xml
```

---

**Happy coding! Always run checks before pushing.** ✨
