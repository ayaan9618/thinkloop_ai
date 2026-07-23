# Makefile for thinkloop AI project
# Run: make <target>

.PHONY: help install setup dev test lint format secure build clean docker docker-up docker-down docs

help:
	@echo "thinkloop AI - Available Commands"
	@echo "=================================="
	@echo "make install       - Install dependencies"
	@echo "make setup         - Setup development environment"
	@echo "make dev           - Run development server"
	@echo "make test          - Run tests"
	@echo "make test-cov      - Run tests with coverage"
	@echo "make lint          - Run all linting checks"
	@echo "make format        - Format code with Black"
	@echo "make format-check  - Check formatting"
	@echo "make secure        - Run security scan"
	@echo "make precommit     - Run all pre-commit checks"
	@echo "make clean         - Clean build artifacts"
	@echo "make docker-build  - Build Docker image"
	@echo "make docker-up     - Start Docker services"
	@echo "make docker-down   - Stop Docker services"
	@echo "make docs          - Generate documentation"
	@echo "make db-reset      - Reset database"

# Setup
install:
	pip install -r requirements.txt

setup: install
	cp .env.example .env 2>/dev/null || true
	mkdir -p logs
	@echo "✅ Setup complete!"

# Development
dev:
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Testing
test:
	pytest backend/tests/ -v

test-cov:
	pytest backend/tests/ \
		--cov=backend \
		--cov-report=html \
		--cov-report=term-missing \
		--cov-fail-under=80

test-fast:
	pytest backend/tests/ -v --tb=short

test-watch:
	ptw backend/tests/

# Linting
lint: lint-flake8 lint-mypy lint-black
	@echo "✅ All linting checks passed!"

lint-flake8:
	flake8 backend/ --max-line-length=100 --exclude=__pycache__,migrations

lint-mypy:
	mypy backend/ --ignore-missing-imports --no-implicit-optional

lint-black:
	black backend/ --check --line-length=100

# Formatting
format:
	black backend/ --line-length=100
	isort backend/ --profile black --line-length=100
	@echo "✅ Code formatted!"

format-check:
	black backend/ --check --line-length=100

# Security
secure:
	bandit -r backend/ -f json -o bandit-report.json
	@echo "✅ Security scan complete! Check bandit-report.json"

# Pre-commit
precommit: format lint secure test-cov
	@echo "✅ All pre-commit checks passed!"

# Clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name ".mypy_cache" -delete
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -delete
	find . -type d -name "dist" -delete
	find . -type d -name "build" -delete
	find . -type f -name ".DS_Store" -delete
	@echo "✅ Clean complete!"

# Docker
docker-build:
	docker build -t thinkloop-ai:latest .

docker-up:
	docker-compose up -d
	@echo "✅ Docker services started!"
	@echo "   MySQL:    localhost:3306"
	@echo "   Redis:    localhost:6379"
	@echo "   API:      localhost:8000"
	@echo "   Docs:     http://localhost:8000/docs"

docker-down:
	docker-compose down
	@echo "✅ Docker services stopped!"

docker-logs:
	docker-compose logs -f backend

# Database
db-reset:
	docker-compose down -v
	docker-compose up -d mysql
	sleep 5
	docker-compose run backend python -c "from backend.app.database import init_db; init_db()"
	@echo "✅ Database reset!"

db-migrate:
	alembic upgrade head

# Documentation
docs:
	@echo "Generating documentation..."
	@echo "See docs/ directory for API_SPEC.md, DATABASE_DESIGN.md, etc."

# Utilities
ps:
	docker-compose ps

logs:
	docker-compose logs -f

shell:
	docker-compose run backend python

freeze:
	pip freeze > requirements.txt

version:
	@python --version
	@echo "pip: $$(pip --version)"

# Advanced
coverage-html: test-cov
	@echo "Opening coverage report..."
	@python -c "import webbrowser; webbrowser.open('htmlcov/index.html')"

check-deps:
	pip list --outdated

update-deps:
	pip install --upgrade -r requirements.txt

security-check:
	pip-audit

# CI
ci: lint secure test-cov
	@echo "✅ CI checks passed!"

# Default
.DEFAULT_GOAL := help
