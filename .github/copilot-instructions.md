# GitHub Copilot Instructions for thinkloop AI
# Place in .github/copilot-instructions.md

You are an AI coding assistant for the **thinkloop AI** project - an Intelligent Tutoring System using the Socratic Method.

## Project Context

**What is thinkloop AI?**
An AI-powered tutoring system inspired by Harvard CS50 AI that teaches through questioning and guidance rather than direct answers.

**Tech Stack**:
- **Backend**: Python, FastAPI, Uvicorn, SQLAlchemy
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Database**: MySQL on AWS RDS
- **Cloud**: AWS Elastic Beanstalk
- **AI**: OpenAI API (GPT-4/GPT-3.5)

---

## Core Principles

1. **Socratic Method First**: Always prioritize teaching through questioning
2. **API-Centric**: All features exposed via REST API first
3. **Security**: Authentication required for all endpoints except `/auth/*`
4. **Quality**: Comprehensive testing, type hints, documentation
5. **Performance**: <500ms API response time, <2s frontend load

---

## Directory Structure Reference

```
backend/app/
├── api/              # Route handlers → /api/v1/*
├── services/         # Business logic
├── models/           # SQLAlchemy ORM models
├── schemas/          # Pydantic validation schemas
└── prompts/          # AI prompt templates

frontend/
├── index.html        # Main entry point
└── js/               # Vanilla JavaScript modules
```

---

## When Writing Backend Code

### 1. API Endpoints

- ✓ Use `@router.get()`, `@router.post()`, etc.
- ✓ Always specify `response_model` with Pydantic schemas
- ✓ Add JWT authentication: `current_user: User = Depends(get_current_user)`
- ✓ Include docstrings explaining purpose, args, returns, raises
- ✓ Use type hints on all parameters and return values

### 2. Services Layer

- ✓ Keep business logic in services, not routes
- ✓ Use dependency injection for databases and AI service
- ✓ Raise meaningful exceptions for error handling
- ✓ Write docstrings with Args, Returns, Raises sections

### 3. Database & Models

- ✓ Use SQLAlchemy ORM (never raw SQL)
- ✓ Add indexes on frequently queried columns
- ✓ Include proper relationships and foreign keys
- ✓ Create migrations with Alembic for schema changes

### 4. Testing

- ✓ Write tests for every new service method
- ✓ Aim for 80%+ code coverage
- ✓ Use pytest fixtures for setup
- ✓ Include both happy path and error scenarios

---

## When Writing Frontend Code

### 1. HTML Structure

- ✓ Use semantic HTML (`<header>`, `<main>`, `<footer>`, `<article>`, etc.)
- ✓ Add `id` attributes to interactive elements
- ✓ Include proper `<label>` tags for all form inputs
- ✓ Add `alt` attributes to images

### 2. Styling with Tailwind

- ✓ Use Tailwind utility classes (not custom CSS)
- ✓ Responsive classes: `md:` and `lg:` prefixes
- ✓ Color palette: Blues for primary, grays for neutral
- ✓ Spacing: Use Tailwind scale (4px base unit)

### 3. JavaScript

- ✓ Use modules (separate concerns into different files)
- ✓ Use `async/await` for async operations
- ✓ Event delegation for dynamic elements
- ✓ Call API through centralized `api.js` module

---

## Common Tasks & Examples

### Adding a New API Endpoint

```python
# 1. Create schema in schemas/
class AskQuestionRequest(BaseModel):
    question: str = Field(..., max_length=5000)
    session_id: Optional[str] = None

class AskQuestionResponse(BaseModel):
    response: str
    hint_level: int
    conversation_id: str

# 2. Create service method in services/
class TutorService:
    async def process_question(self, user_id: str, question: str):
        # Business logic here
        pass

# 3. Create route in api/
@router.post("/tutor/ask", response_model=AskQuestionResponse)
async def ask_question(
    request: AskQuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TutorService(db)
    return await service.process_question(current_user.user_id, request.question)
```

### Adding a New Frontend Page

```javascript
// 1. Create HTML in index.html
<main id="tutor-page" class="hidden">
  <div class="max-w-2xl mx-auto p-4">
    <h1 class="text-3xl font-bold mb-6">Ask Your Question</h1>
    <form id="question-form">
      <!-- Form fields -->
    </form>
  </div>
</main>

// 2. Create JavaScript module in js/
export async function initTutorPage() {
  const form = document.getElementById('question-form');
  form.addEventListener('submit', handleQuestionSubmit);
}

async function handleQuestionSubmit(e) {
  e.preventDefault();
  const question = e.target.question.value;
  const response = await api.tutor.ask(question);
  displayResponse(response);
}

// 3. Call from app.js router
router.on('tutor', () => {
  initTutorPage();
});
```

---

## Testing Quick Reference

```bash
# Run all tests
pytest backend/tests/

# Run specific test
pytest backend/tests/test_tutor.py::test_ask_question

# Run with coverage
pytest --cov=backend --cov-report=html

# Format code
black backend/

# Lint code
flake8 backend/

# Type check
mypy backend/
```

---

## API Conventions

### Request Format

```json
{
  "question": "How does binary search work?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Response Format

```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440001",
  "response": "Great question! Let me ask you first...",
  "hint_level": 0,
  "can_request_hint": true
}
```

### Error Response Format

```json
{
  "error": "INVALID_INPUT",
  "message": "Question must be between 1 and 5000 characters",
  "details": {
    "field": "question",
    "constraint": "length"
  }
}
```

---

## Security Reminders

- ✓ Never commit `.env` files
- ✓ Always hash passwords with bcrypt
- ✓ Validate JWT tokens on protected endpoints
- ✓ Use parameterized queries (SQLAlchemy does this)
- ✓ Escape HTML output
- ✓ No sensitive data in logs
- ✓ HTTPS only in production
- ✓ Rate limiting on all endpoints

---

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make commits
git add .
git commit -m "feat: implement new feature"

# Push and create PR
git push origin feature/new-feature

# After approval and tests pass
git checkout develop
git merge feature/new-feature
git push origin develop
```

---

## Documentation Requirements

- ✓ Docstrings on all public functions
- ✓ Type hints on all functions
- ✓ Comments explaining "why", not "what"
- ✓ Update API_SPEC.md for new endpoints
- ✓ Update DATABASE_DESIGN.md for schema changes
- ✓ Keep README.md current

---

## Performance Targets

- API response time (p95): < 500ms
- Database query time (p95): < 100ms
- Frontend load time: < 2 seconds
- Lighthouse score: > 90
- Code coverage: 80%+
- Uptime: 99.9%

---

## When in Doubt

1. Check existing similar implementations in codebase
2. Follow patterns already established
3. Read `/docs/API_SPEC.md` for API reference
4. Read `CONTRIBUTING.md` for guidelines
5. Ask in GitHub Discussions if unsure

---

## Helpful Shortcuts

| Task | Command |
|------|---------|
| Format code | `black backend/` |
| Lint | `flake8 backend/` |
| Type check | `mypy backend/` |
| Test | `pytest backend/tests/` |
| Test coverage | `pytest --cov=backend` |
| Security scan | `bandit -r backend/` |
| Run app | `uvicorn backend.app.main:app --reload` |

---

**Last Updated**: July 2026  
**Version**: 1.0  
**Maintained By**: Engineering Team

For project-specific questions, check:
- `README.md` - Overview and setup
- `PRD.md` - Product requirements
- `docs/API_SPEC.md` - API reference
- `CONTRIBUTING.md` - Development guidelines
