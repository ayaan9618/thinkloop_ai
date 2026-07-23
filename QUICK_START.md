# Quick Start Guide - thinkloop AI

**Last Updated**: July 2026  
**Status**: Ready for Development

---

## 📁 Project Structure Overview

```
thinkloop_ai/
├── README.md                        # Start here!
├── PRD.md                           # What to build
├── ROADMAP.md                       # When to build it
├── PROJECT_SETUP_COMPLETE.md        # This foundation
│
├── docs/                            # 📚 Documentation
│   ├── SYSTEM_DESIGN.md             # Architecture
│   ├── DATABASE_DESIGN.md           # Schema
│   ├── API_SPEC.md                  # Endpoints
│   └── PROMPTS.md                   # AI guidance
│
├── backend/                         # 🐍 Python Backend
│   └── app/
│       ├── api/                     # Route handlers
│       ├── services/                # Business logic
│       ├── models/                  # Database models
│       ├── schemas/                 # Request/response
│       └── prompts/                 # AI prompts
│
├── frontend/                        # 🌐 Frontend
│   ├── index.html                   # Main page
│   ├── css/
│   │   └── styles.css               # Tailwind styles
│   └── js/                          # Modules
│       ├── app.js                   # Main app
│       ├── api.js                   # API client
│       ├── auth.js                  # Authentication
│       └── router.js                # Navigation
│
├── agents/                          # 🤖 AI Instructions
│   ├── backend-agent.md             # Backend guidelines
│   └── frontend-agent.md            # Frontend guidelines
│
├── .github/                         # GitHub config
│   └── copilot-instructions.md      # Copilot config
│
├── .env.example                     # Environment template
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Project config
├── .gitignore                       # Git ignore
├── .editorconfig                    # Editor config
└── .pre-commit-config.yaml          # Git hooks
```

---

## 🚀 Getting Started (5 Steps)

### 1️⃣ Setup Local Environment
```bash
# Clone and navigate to project
cd thinkloop_ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration
```

### 2️⃣ Setup Database
```bash
# Initialize database (MySQL)
# Ensure MySQL is running locally

# Create database
mysql -u root -p -e "CREATE DATABASE thinkloop_ai;"

# Update DATABASE_URL in .env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/thinkloop_ai

# Run migrations
alembic upgrade head
```

### 3️⃣ Start Backend Server
```bash
# Development mode with auto-reload
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Server runs at: http://localhost:8000
# API docs at: http://localhost:8000/docs (Swagger UI)
```

### 4️⃣ Start Frontend
```bash
# Open in browser
# http://localhost:3000  (if using dev server)
# or
# Open frontend/index.html directly in browser
```

### 5️⃣ Run Tests
```bash
# Run all tests
pytest backend/tests/ -v

# Run with coverage
pytest --cov=backend --cov-report=html

# View coverage report
open htmlcov/index.html
```

---

## 📚 Essential Reading

| Document | Purpose | Read When |
|----------|---------|-----------|
| [README.md](README.md) | Project overview | First |
| [PRD.md](PRD.md) | What to build | Planning features |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to code | Before coding |
| [docs/API_SPEC.md](docs/API_SPEC.md) | API contracts | Building backends |
| [docs/DATABASE_DESIGN.md](docs/DATABASE_DESIGN.md) | Database schema | Building database |
| [agents/backend-agent.md](agents/backend-agent.md) | Backend patterns | Backend development |
| [agents/frontend-agent.md](agents/frontend-agent.md) | Frontend patterns | Frontend development |
| [SECURITY.md](SECURITY.md) | Security | Building auth |

---

## 🛠️ Development Commands

### Code Quality
```bash
# Format code
black backend/

# Lint code
flake8 backend/

# Type checking
mypy backend/

# Security scan
bandit -r backend/
```

### Testing
```bash
# Run all tests
pytest

# Run specific test
pytest backend/tests/test_auth.py::test_login

# Run with verbose output
pytest -vv

# Run only unit tests
pytest -m unit

# Run with coverage
pytest --cov=backend
```

### Database
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat: add my feature"

# Push to GitHub
git push origin feature/my-feature

# Create Pull Request on GitHub
# (After tests pass, merge to develop)
```

---

## 📋 Development Phases

**Phase 1 (Weeks 1-8): Foundation**
- [ ] Infrastructure setup
- [ ] Authentication (JWT + OAuth2)
- [ ] Database foundation
- [ ] AI engine MVP

**Phase 2 (Weeks 9-16): Tutor Engine**
- [ ] Hint system (6 levels)
- [ ] Misconception detection
- [ ] Session management
- [ ] Analytics foundation

**Phase 3 (Weeks 17-24): Frontend**
- [ ] Responsive design
- [ ] Interactive components
- [ ] Client-side routing
- [ ] API integration

**Phase 4+ (After Week 24): Advanced**
- [ ] Advanced features
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Deployment

---

## 🔐 Security Checklist

Before committing:
- [ ] No `.env` file in git
- [ ] No hardcoded secrets
- [ ] All endpoints authenticated
- [ ] Input validation on forms
- [ ] HTTPS configured
- [ ] Secrets in AWS Secrets Manager

---

## 📊 Key Metrics

| Metric | Target | Current |
|--------|--------|---------|
| API Response Time (p95) | < 500ms | TBD |
| Frontend Load Time | < 2s | TBD |
| Code Coverage | 80%+ | TBD |
| Lighthouse Score | > 90 | TBD |
| Uptime | 99.9% | TBD |

---

## 🆘 Troubleshooting

### ImportError: No module named 'backend'
```bash
# Add backend to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/thinkloop_ai"
# or
python -m uvicorn backend.app.main:app
```

### Database Connection Error
```bash
# Check MySQL is running
mysql -u root -p

# Check DATABASE_URL in .env
# Format: mysql+pymysql://user:password@host:port/database

# Test connection
python -c "from sqlalchemy import create_engine; engine = create_engine(DATABASE_URL); print(engine.connect())"
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn backend.app.main:app --port 8001
```

### Tests Failing
```bash
# Clear cache
rm -rf .pytest_cache __pycache__

# Run with verbose output
pytest -vv

# Run specific test
pytest backend/tests/test_file.py::test_function
```

---

## 📞 Important Files to Know

| File | Purpose |
|------|---------|
| `.env` | Environment variables (⚠️ Never commit) |
| `backend/app/main.py` | FastAPI app initialization |
| `backend/app/api/auth.py` | Authentication endpoints |
| `backend/app/models/user.py` | User database model |
| `frontend/index.html` | Main HTML file |
| `frontend/js/api.js` | API client |
| `pyproject.toml` | Project configuration |
| `requirements.txt` | Python dependencies |

---

## ✅ Before Going to Production

- [ ] Security audit passed
- [ ] All tests passing (80%+ coverage)
- [ ] Code review completed
- [ ] Database backups configured
- [ ] Monitoring/alerts setup
- [ ] Error tracking (Sentry) enabled
- [ ] Rate limiting configured
- [ ] HTTPS/SSL certificates ready
- [ ] AWS Elastic Beanstalk configured
- [ ] Environment variables secured

---

## 📖 Documentation Links

- **Architecture**: [SYSTEM_DESIGN.md](docs/SYSTEM_DESIGN.md)
- **Database**: [DATABASE_DESIGN.md](docs/DATABASE_DESIGN.md)
- **API**: [API_SPEC.md](docs/API_SPEC.md)
- **AI Prompts**: [PROMPTS.md](docs/PROMPTS.md)
- **Timeline**: [ROADMAP.md](ROADMAP.md)
- **Coding**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Security**: [SECURITY.md](SECURITY.md)

---

## 🎯 Current Status

✅ **Documentation Complete** - All specifications defined  
✅ **Architecture Designed** - System ready to build  
✅ **Database Planned** - Schema ready to implement  
✅ **API Specified** - Endpoints ready to code  
✅ **Dev Environment Ready** - Dependencies listed  
⏳ **Implementation Pending** - Ready to start Phase 1  

---

**Ready to build? Start with Phase 1: Backend Foundation**

Questions? Check the relevant documentation or agent guidelines.

**Happy coding! 🚀**

---

**Version**: 1.0.0-alpha  
**Last Updated**: July 2026  
**Project**: thinkloop AI
