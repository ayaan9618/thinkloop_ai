# Contributing Guidelines
# thinkloop AI

**Version**: 1.0  
**Last Updated**: July 2026

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Code Standards](#code-standards)
3. [Git Workflow](#git-workflow)
4. [Pull Request Process](#pull-request-process)
5. [Commit Messages](#commit-messages)
6. [Testing](#testing)
7. [Documentation](#documentation)
8. [Code Review](#code-review)

---

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- Virtual environment (venv or virtualenv)
- Docker (optional)

### Development Setup

```bash
# 1. Clone repository
git clone https://github.com/ayaan9618/thinkloop_ai.git
cd thinkloop_ai

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Set up pre-commit hooks
pre-commit install

# 5. Create local .env
cp .env.example .env
# Edit .env with local configuration

# 6. Initialize database
alembic upgrade head

# 7. Run tests to verify setup
pytest

# 8. Start development server
uvicorn backend.app.main:app --reload
```

---

## Code Standards

### Python Style Guide

We follow **PEP 8** with these enforcements:

#### Formatting

- **Line Length**: 100 characters max
- **Indentation**: 4 spaces
- **Imports**: Organized in groups (stdlib, third-party, local)

```python
# ✓ Good
import os
import sys
from typing import Optional, List

import fastapi
import pydantic

from backend.app import models
from backend.app.utils import validators
```

- **Naming Conventions**:

```python
# Constants - UPPER_SNAKE_CASE
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30

# Classes - PascalCase
class UserService:
    pass

# Functions/Methods - snake_case
def get_user_by_id(user_id: str) -> User:
    pass

# Variables - snake_case
total_users = 100
```

#### Type Hints

All functions must have type hints:

```python
# ✓ Good
def calculate_score(responses: List[str], weights: Dict[str, float]) -> float:
    """Calculate overall score from responses."""
    pass

# ✗ Bad
def calculate_score(responses, weights):
    """Calculate overall score from responses."""
    pass
```

#### Docstrings

Use Google-style docstrings:

```python
def create_session(user_id: str, topic: str) -> Session:
    """Create a new learning session.
    
    Args:
        user_id: UUID of the user creating the session
        topic: Learning topic for the session
        
    Returns:
        Session object with generated session_id
        
    Raises:
        ValueError: If topic is not valid
        DatabaseError: If database write fails
    """
    pass
```

#### Comments

- Write comments for **why**, not **what**
- Keep comments up-to-date
- Avoid stating the obvious

```python
# ✓ Good
# Limit to 100 to prevent excessive memory usage during batch processing
results = results[:100]

# ✗ Bad
# Set results to first 100 items
results = results[:100]
```

### Code Quality Tools

All code must pass these checks:

```bash
# Format code
black backend/

# Lint code
flake8 backend/ --max-line-length=100

# Type checking
mypy backend/

# Security check
bandit -r backend/
```

These are enforced in CI/CD pipeline.

---

## Git Workflow

### Branch Naming

Use descriptive branch names with prefixes:

```
feature/user-authentication
feature/hint-system-v2
bugfix/jwt-token-expiration
hotfix/critical-security-issue
docs/api-documentation
refactor/session-service
test/integration-tests
```

### Main Branches

- **main**: Production-ready code, protected branch
- **develop**: Development integration branch
- **staging**: Staging environment code

### Feature Branch Workflow

1. Create feature branch from `develop`
2. Make changes with descriptive commits
3. Push branch and create pull request
4. Get code review approval
5. Pass all CI checks
6. Merge to `develop`
7. Periodically merge `develop` → `main`

```bash
# Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/new-feature-name

# Make commits
git add .
git commit -m "feat: implement new feature"

# Push branch
git push origin feature/new-feature-name

# Create PR on GitHub
# After approval and CI passes:
git checkout develop
git pull origin develop
git merge feature/new-feature-name
git push origin develop
```

---

## Pull Request Process

### Before Creating PR

- [ ] Branch is up-to-date with base branch
- [ ] All tests pass locally: `pytest`
- [ ] Code passes linting: `black`, `flake8`, `mypy`
- [ ] No new warnings introduced
- [ ] Changes documented in docstrings
- [ ] Database migrations included (if applicable)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #(issue number)
Related to #(issue number)

## Changes Made
- Specific change 1
- Specific change 2

## Testing
Describe testing approach:
- Manual testing done
- Unit tests added
- Integration tests added

## Checklist
- [ ] My code follows style guidelines
- [ ] I have performed a self-review
- [ ] I have commented complex code
- [ ] I have made documentation changes
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New tests pass locally
- [ ] No migration reversions needed
```

### PR Review Requirements

- Minimum 1 approval from code owner
- All CI checks pass
- 0 blocking comments
- Documentation updated if needed

### Code Review Comments

Constructive feedback format:

```markdown
### Suggestion
In `auth_service.py` line 45, consider using a context manager:

Before:
```python
conn = get_connection()
try:
    # do something
finally:
    conn.close()
```

After:
```python
with get_connection() as conn:
    # do something
```

This is cleaner and ensures cleanup.
```

---

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without feature/bug changes
- `perf`: Performance improvement
- `test`: Test additions/changes
- `chore`: Build system, dependencies, etc.

### Examples

```bash
# Feature
git commit -m "feat(auth): implement JWT token refresh mechanism"

# Bug fix
git commit -m "fix(tutor): prevent hint level overflow in hint escalation"

# Documentation
git commit -m "docs(api): add authentication endpoint examples"

# Multiple line commit
git commit -m "feat(session): implement session persistence

- Add session save functionality
- Persist conversation history
- Add session resumption feature
- Update database schema with session table

Closes #123"
```

### Commit Message Guidelines

- Use imperative mood: "add feature" not "added feature"
- Don't capitalize first letter
- Limit to 50 characters for subject line
- Reference issues: "Fixes #123" or "Relates to #456"
- Explain **why**, not **what**
- Wrap body at 72 characters
- Separate subject and body with blank line

---

## Testing

### Test Organization

```
backend/tests/
├── __init__.py
├── conftest.py              # Pytest fixtures
├── test_auth.py             # Auth tests
├── test_tutor.py            # Tutor tests
├── test_api.py              # API endpoint tests
├── integration/
│   └── test_full_flow.py    # End-to-end tests
└── unit/
    ├── test_services.py
    └── test_utils.py
```

### Writing Tests

Use pytest with fixtures:

```python
import pytest
from backend.app.services import TutorService
from backend.app import models

@pytest.fixture
def tutor_service(db_session):
    """Create a TutorService instance."""
    return TutorService(db_session)

@pytest.fixture
def sample_user(db_session):
    """Create a sample user."""
    user = models.User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    return user

def test_process_question_returns_response(tutor_service, sample_user):
    """Test that tutor returns response to question."""
    response = tutor_service.process_question(
        user_id=sample_user.user_id,
        question="How does binary search work?"
    )
    
    assert response is not None
    assert response.hint_level == 0
    assert len(response.response) > 0
```

### Test Coverage

- Minimum 80% code coverage required
- All new features must include tests
- All bug fixes must include regression tests

```bash
# Run tests with coverage
pytest --cov=backend --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest backend/tests/test_auth.py

# Run specific test
pytest backend/tests/test_auth.py::test_user_registration

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x

# Run with markers
pytest -m "not integration"
```

---

## Documentation

### Code Documentation

- All public functions must have docstrings
- All classes must have docstrings
- Complex logic must have inline comments

### API Documentation

- Update `/docs/API_SPEC.md` when adding endpoints
- Include request/response examples
- Document error codes and meanings
- Update OpenAPI spec

### Database Documentation

- Document schema changes in migration files
- Update `docs/DATABASE_DESIGN.md` with changes
- Include rationale for structural changes

### Architectural Documentation

- Document design decisions in `docs/ARCHITECTURE_DECISIONS.md`
- Use ADR (Architecture Decision Record) format
- Include alternatives considered and tradeoffs

---

## Code Review Checklist

As a reviewer, check:

- [ ] **Functionality**: Does it do what it claims?
- [ ] **Tests**: Are there tests? Do they pass?
- [ ] **Code Quality**: Does it follow standards?
- [ ] **Performance**: Are there obvious performance issues?
- [ ] **Security**: Any security vulnerabilities?
- [ ] **Documentation**: Is it documented?
- [ ] **Edge Cases**: Are edge cases handled?
- [ ] **Backwards Compatibility**: Does it break anything?

---

## Common Issues & Solutions

### Issue: Tests fail locally but pass in CI

**Solution**:
- Ensure you're using same Python version as CI
- Clear cache: `rm -rf .pytest_cache`
- Reset database: `alembic downgrade base && alembic upgrade head`
- Check environment variables match CI

### Issue: Pre-commit hooks blocking commits

**Solution**:
```bash
# Run pre-commit manually to see issues
pre-commit run --all-files

# Fix formatting issues
black .
flake8 . --fix-long-lines

# Commit after fixes
git add .
git commit -m "..."
```

### Issue: Merge conflicts

**Solution**:
```bash
# Pull latest develop
git fetch origin
git rebase origin/develop

# Resolve conflicts in your editor
# After resolving:
git add .
git rebase --continue
```

---

## Getting Help

- **Questions**: Create GitHub Discussions
- **Bugs**: File GitHub Issues with reproduction steps
- **Security**: Email security@thinkloop.ai (do not create public issues)
- **Chat**: Join our Discord community

---

## Code of Conduct

- Be respectful and inclusive
- Welcome different perspectives
- Give credit where due
- Focus on ideas, not personalities
- Help others grow and learn

---

**Document Owner**: Engineering Team  
**Last Updated**: July 2026
