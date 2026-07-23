# Project Structure & Organization
# thinkloop AI

**Version**: 1.0  
**Last Updated**: July 2026

---

## Directory Tree

```
thinkloop_ai/
│
├── README.md                           # Main project overview
├── PRD.md                              # Product requirements document
├── CONTRIBUTING.md                     # Contribution guidelines
├── CHANGELOG.md                        # Version history and releases
├── LICENSE                             # MIT License
│
├── backend/                            # Python FastAPI backend
│   ├── app/                           # Main application code
│   │   ├── __init__.py               # Package init
│   │   ├── main.py                   # FastAPI app initialization
│   │   ├── config.py                 # Configuration management
│   │   ├── dependencies.py           # Dependency injection
│   │   │
│   │   ├── models/                   # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py               # User model
│   │   │   ├── session.py            # Session model
│   │   │   ├── conversation.py       # Conversation model
│   │   │   ├── hint.py               # Hint model
│   │   │   ├── misconception.py      # Misconception model
│   │   │   ├── analytics.py          # Analytics model
│   │   │   └── refresh_token.py      # Refresh token model
│   │   │
│   │   ├── schemas/                  # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py               # User schemas
│   │   │   ├── auth.py               # Authentication schemas
│   │   │   ├── session.py            # Session schemas
│   │   │   ├── conversation.py       # Conversation schemas
│   │   │   ├── tutor.py              # Tutor interaction schemas
│   │   │   └── analytics.py          # Analytics schemas
│   │   │
│   │   ├── api/                      # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py               # /api/v1/auth routes
│   │   │   ├── tutor.py              # /api/v1/tutor routes
│   │   │   ├── sessions.py           # /api/v1/sessions routes
│   │   │   ├── analytics.py          # /api/v1/analytics routes
│   │   │   ├── admin.py              # /api/v1/admin routes (admin only)
│   │   │   └── health.py             # /health endpoint
│   │   │
│   │   ├── services/                 # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py       # Authentication logic
│   │   │   ├── tutor_service.py      # Main tutor logic
│   │   │   ├── ai_service.py         # OpenAI API integration
│   │   │   ├── conversation_service.py # Conversation management
│   │   │   ├── hint_service.py       # Hint generation and management
│   │   │   ├── session_service.py    # Session management
│   │   │   ├── analytics_service.py  # Analytics processing
│   │   │   └── user_service.py       # User management
│   │   │
│   │   ├── utils/                    # Utility modules
│   │   │   ├── __init__.py
│   │   │   ├── jwt_utils.py          # JWT token utilities
│   │   │   ├── password_utils.py     # Password hashing
│   │   │   ├── validators.py         # Input validation
│   │   │   ├── errors.py             # Custom exceptions
│   │   │   └── logging_config.py     # Logging setup
│   │   │
│   │   ├── middleware/               # Custom middleware
│   │   │   ├── __init__.py
│   │   │   ├── error_handler.py      # Global error handling
│   │   │   ├── request_logger.py     # Request/response logging
│   │   │   ├── rate_limiter.py       # Rate limiting
│   │   │   └── cors_handler.py       # CORS configuration
│   │   │
│   │   ├── prompts/                  # AI prompt templates
│   │   │   ├── __init__.py
│   │   │   ├── system_prompt.py      # Master system prompt
│   │   │   ├── tutor_prompts.py      # Socratic question prompts
│   │   │   ├── hint_prompts.py       # Hint generation prompts
│   │   │   ├── misconception_prompts.py
│   │   │   └── debug_prompts.py
│   │   │
│   │   └── constants/                # Application constants
│   │       ├── __init__.py
│   │       ├── enums.py              # Enum definitions
│   │       └── messages.py           # User-facing messages
│   │
│   ├── tests/                        # Test suite
│   │   ├── __init__.py
│   │   ├── conftest.py               # Pytest fixtures and configuration
│   │   ├── test_auth.py              # Authentication tests
│   │   ├── test_tutor.py             # Tutor logic tests
│   │   ├── test_api.py               # API endpoint tests
│   │   ├── test_services.py          # Service layer tests
│   │   ├── unit/                     # Unit tests
│   │   │   ├── test_jwt_utils.py
│   │   │   ├── test_validators.py
│   │   │   └── test_password_utils.py
│   │   ├── integration/              # Integration tests
│   │   │   ├── test_full_flow.py
│   │   │   └── test_api_flow.py
│   │   └── mocks/                    # Mock objects
│   │       └── mock_openai.py
│   │
│   ├── migrations/                   # Alembic database migrations
│   │   ├── versions/
│   │   │   ├── 001_create_initial_schema.py
│   │   │   ├── 002_add_indexes.py
│   │   │   └── ...
│   │   ├── env.py                    # Alembic environment config
│   │   └── script.py.mako            # Migration template
│   │
│   ├── scripts/                      # Utility scripts
│   │   ├── __init__.py
│   │   ├── seed_db.py                # Database seeding
│   │   ├── create_admin.py           # Create admin user
│   │   ├── migrate_data.py           # Data migration utilities
│   │   └── cleanup.py                # Cleanup utilities
│   │
│   ├── requirements.txt              # Python dependencies
│   ├── requirements-dev.txt          # Development dependencies
│   ├── pyproject.toml                # Python project metadata
│   └── pytest.ini                    # Pytest configuration
│
├── frontend/                         # Frontend application
│   ├── index.html                   # Main HTML entry point
│   ├── index.js                     # Entry point script
│   │
│   ├── css/
│   │   ├── styles.css               # Tailwind compiled CSS
│   │   └── tailwind.config.js        # Tailwind configuration
│   │
│   ├── js/
│   │   ├── app.js                   # Main application logic
│   │   ├── api.js                   # API client wrapper
│   │   ├── auth.js                  # Authentication handler
│   │   ├── ui.js                    # UI interactions
│   │   ├── storage.js               # Local storage management
│   │   ├── router.js                # Client-side routing
│   │   └── utils.js                 # Utility functions
│   │
│   ├── components/                  # Reusable components
│   │   ├── header.js
│   │   ├── tutor-interface.js
│   │   ├── session-list.js
│   │   └── analytics-dashboard.js
│   │
│   ├── assets/
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   │
│   ├── package.json
│   └── package-lock.json
│
├── docs/                            # Documentation
│   ├── SYSTEM_DESIGN.md             # System architecture
│   ├── DATABASE_DESIGN.md           # Database schema
│   ├── API_SPEC.md                  # API documentation
│   ├── PROMPTS.md                   # AI prompts guide
│   ├── ARCHITECTURE_DECISIONS.md    # ADR format decisions
│   ├── DEPLOYMENT.md                # Deployment guide
│   ├── TESTING.md                   # Testing strategy
│   ├── SECURITY.md                  # Security guidelines
│   ├── STYLE_GUIDE.md               # Code style guide
│   ├── ERROR_HANDLING.md            # Error handling patterns
│   ├── OBSERVABILITY.md             # Logging and monitoring
│   ├── ROADMAP.md                   # Development roadmap
│   ├── FEATURES.md                  # Feature inventory
│   └── AI_BEHAVIOR.md               # AI tutor behavior spec
│
├── agents/                          # AI agent instructions
│   ├── backend-agent.md             # Backend development agent
│   ├── frontend-agent.md            # Frontend development agent
│   ├── database-agent.md            # Database schema agent
│   ├── aws-agent.md                 # AWS/DevOps agent
│   ├── testing-agent.md             # Testing agent
│   ├── documentation-agent.md       # Documentation agent
│   ├── prompt-engineer-agent.md     # Prompt engineering agent
│   ├── security-agent.md            # Security review agent
│   ├── reviewer-agent.md            # Code review agent
│   └── planner-agent.md             # Project planning agent
│
├── .github/                         # GitHub configuration
│   ├── copilot-instructions.md      # GitHub Copilot instructions
│   ├── workflows/
│   │   ├── ci.yml                   # CI/CD pipeline
│   │   ├── deploy.yml               # Deployment workflow
│   │   └── tests.yml                # Test workflow
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
│
├── .cursor/                         # Cursor IDE configuration
│   ├── rules.md                     # Cursor-specific rules
│   └── .cursorrules                 # Cursor rules file
│
├── .claude.md                       # Claude AI instructions
├── .gemini.md                       # Gemini AI instructions
├── .cursorrules                     # Cursor rules
├── .editorconfig                    # Editor configuration
├── .gitignore                       # Git ignore rules
├── .pre-commit-config.yaml          # Pre-commit hooks
├── .env.example                     # Example environment file
├── pyproject.toml                   # Python project config
├── Makefile                         # Development commands
└── docker-compose.yml               # Docker compose for local dev
```

---

## Directory Descriptions

### `/backend`

Main Python application code using FastAPI.

**Key Subdirectories**:
- `app/`: Core application logic
- `tests/`: Test suite with unit and integration tests
- `migrations/`: Database schema migrations (Alembic)
- `scripts/`: Utility and maintenance scripts

### `/frontend`

Frontend application (HTML5, CSS, vanilla JavaScript).

**Key Files**:
- `index.html`: Main entry point
- `js/`: JavaScript modules
- `css/`: Tailwind CSS
- `components/`: Reusable UI components

### `/docs`

Comprehensive documentation of system.

**Key Documents**:
- `SYSTEM_DESIGN.md`: Architecture and data flows
- `API_SPEC.md`: Complete API endpoint reference
- `DATABASE_DESIGN.md`: Schema and relationships
- `PROMPTS.md`: AI prompt engineering guide

### `/agents`

Instructions for AI coding agents (Copilot, Claude, Cursor).

**Agent Types**:
- Development agents (backend, frontend, database)
- Infrastructure agents (AWS, DevOps)
- Quality agents (testing, security, reviewer)
- Supporting agents (documentation, planner)

### `/.github`

GitHub-specific configuration and workflows.

**Contents**:
- GitHub Actions workflows (CI/CD)
- Issue and PR templates
- Copilot instructions

### `/.cursor`

Cursor IDE-specific configuration.

**Contents**:
- Custom rules for Cursor AI
- Code generation settings

---

## File Organization Principles

### 1. Modularity
- Each module has a single responsibility
- Clear interfaces between modules
- Minimal interdependencies

### 2. Scalability
- Structure supports growth
- Easy to add new features
- Clear where new code belongs

### 3. Testability
- Code organized to be easily testable
- Dependency injection for flexibility
- Clear separation of concerns

### 4. Maintainability
- Consistent structure across codebase
- Clear naming conventions
- Documentation co-located with code

### 5. Navigability
- Intuitive folder structure
- Files named clearly
- Related files grouped together

---

## Common Development Scenarios

### Adding a New Feature

1. Create route in `backend/app/api/`
2. Create request/response schemas in `backend/app/schemas/`
3. Implement logic in `backend/app/services/`
4. Create database model if needed in `backend/app/models/`
5. Write tests in `backend/tests/`
6. Update API docs in `docs/API_SPEC.md`
7. Create migration if needed in `backend/migrations/versions/`

### Adding a New Page to Frontend

1. Create HTML in `frontend/index.html`
2. Create JavaScript module in `frontend/js/`
3. Create UI components in `frontend/components/`
4. Add styles in `frontend/css/`
5. Update routing in `frontend/js/router.js`
6. Call API via `frontend/js/api.js`

### Fixing a Bug

1. Write failing test in `backend/tests/`
2. Fix code in appropriate service/utility
3. Verify test passes
4. Update documentation if behavior changed
5. Create commit with fix reference

### Adding Documentation

1. Create/update `.md` file in `docs/`
2. Follow Markdown formatting standards
3. Include examples where appropriate
4. Link from README or other docs
5. Commit with documentation changes

---

## File Naming Conventions

### Python Files
- **Models**: `{resource}.py` (e.g., `user.py`, `session.py`)
- **Schemas**: `{resource}.py` (e.g., `user.py`)
- **Services**: `{resource}_service.py` (e.g., `auth_service.py`)
- **Routes**: `{resource}.py` (e.g., `tutor.py`)
- **Tests**: `test_{module}.py` (e.g., `test_auth.py`)
- **Utilities**: `{function}_.py` (e.g., `jwt_utils.py`)
- **Migrations**: `{number}_{description}.py`

### Frontend Files
- **HTML**: `{page}.html` (e.g., `index.html`)
- **JS Modules**: `{feature}.js` (e.g., `api.js`)
- **CSS**: `{scope}.css` (e.g., `styles.css`)
- **Components**: `{component-name}.js` (e.g., `tutor-interface.js`)

### Documentation Files
- **Docs**: `{TOPIC}.md` in `docs/` (e.g., `API_SPEC.md`)
- **Agent Instructions**: `{agent}-agent.md` in `agents/`
- **Config**: `{service}.{ext}` (e.g., `.env.example`)

---

## Important Files at a Glance

| File | Purpose |
|------|---------|
| `README.md` | Project overview and setup |
| `PRD.md` | Product requirements |
| `CONTRIBUTING.md` | Development guidelines |
| `backend/app/main.py` | FastAPI application entry |
| `backend/app/config.py` | Configuration management |
| `backend/requirements.txt` | Python dependencies |
| `frontend/index.html` | Frontend entry point |
| `docs/API_SPEC.md` | API reference |
| `docs/DATABASE_DESIGN.md` | Database schema |
| `.env.example` | Environment template |
| `.gitignore` | Git ignore rules |

---

**Document Owner**: Architecture Team  
**Last Updated**: July 2026
