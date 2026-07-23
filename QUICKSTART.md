# Quick Start Guide

## Setup (< 5 minutes)

```bash
# 1. Clone repo
cd thinkloop_ai

# 2. Create .env
cp .env.example .env

# 3. Start MySQL with Docker
docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=thinkloop_ai -p 3306:3306 mysql:8.0

# 4. Install Python packages
pip install -r requirements.txt

# 5. Run backend
python -m uvicorn backend.app.main:app --reload

# 6. Open frontend
open frontend/index.html  # or http://localhost:8000 after backend starts
```

## Backend API Endpoints

**Auth**:
- `POST /api/v1/auth/register` - Create account
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current user

**Tutor**:
- `POST /api/v1/tutor/ask` - Ask question
- `POST /api/v1/tutor/hint/{conversation_id}` - Get hint
- `POST /api/v1/tutor/reveal/{conversation_id}` - Reveal answer

**Health**:
- `GET /health` - Health check
- `GET /docs` - API documentation (Swagger)

## Testing

```bash
# Run all tests
pytest backend/tests/ -v

# Run with coverage
pytest backend/tests/ --cov=backend --cov-fail-under=80

# Run specific test
pytest backend/tests/test_auth.py::test_login_user -v
```

## Code Quality

```bash
# Format code
black backend/ --line-length=100

# Lint
flake8 backend/ --max-line-length=100

# Type check
mypy backend/ --ignore-missing-imports

# Security scan
bandit -r backend/
```

## Frontend Features

- ✅ Login / Register
- ✅ Ask questions to Socratic tutor
- ✅ Request hints
- ✅ Real-time chat interface

## Backend Features

- ✅ JWT authentication
- ✅ Password hashing (bcrypt)
- ✅ MySQL database
- ✅ Socratic method tutor service
- ✅ Test coverage 80%+
- ✅ Type hints

## Architecture

```
backend/app/
├── api/          # Route handlers
├── services/     # Business logic (AuthService, TutorService)
├── models/       # Database models (User, RefreshToken)
├── schemas/      # Request/response validation
└── utils/        # Utilities (JWT, password hashing)

frontend/
├── index.html    # Main page
└── js/
    ├── api.js    # API client
    └── app.js    # UI logic
```

## CI Pipeline

Tests run automatically on push:
- Black formatting check
- Flake8 linting
- MyPy type checking
- Bandit security scan
- Pytest with 80% coverage requirement

---

Ready to code! 🚀
