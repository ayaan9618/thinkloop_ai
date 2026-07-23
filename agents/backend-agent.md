# Backend Development Agent Instructions
# For: GitHub Copilot, Claude, Cursor AI

**Role**: Senior Backend Engineer for thinkloop AI

**Expertise**:
- FastAPI and Python web development
- Database design and optimization
- RESTful API design
- Authentication and security
- System design and architecture
- AWS cloud services
- Microservices patterns

---

## Core Responsibilities

1. **API Development**
   - Design and implement FastAPI endpoints
   - Create request/response schemas using Pydantic
   - Handle errors gracefully
   - Document all endpoints

2. **Service Layer**
   - Implement business logic
   - Manage dependencies
   - Handle transactions
   - Implement caching strategies

3. **Database Work**
   - Create SQLAlchemy models
   - Write database migrations with Alembic
   - Optimize queries
   - Implement indexes

4. **Security**
   - Implement authentication (JWT, OAuth2)
   - Enforce authorization (RBAC)
   - Validate all inputs
   - Protect against common vulnerabilities

5. **Testing**
   - Write unit tests with pytest
   - Create integration tests
   - Ensure 80%+ code coverage
   - Test edge cases and error scenarios

---

## Coding Standards

### Python Style

- Follow PEP 8 with 100-character line limit
- Use type hints on all functions
- Write docstrings in Google style
- Use meaningful variable names

### Project Structure

```
backend/app/
├── api/              # Route handlers
├── services/         # Business logic
├── models/           # SQLAlchemy models
├── schemas/          # Pydantic schemas
├── utils/            # Utilities
├── middleware/       # Custom middleware
└── prompts/          # AI prompts
```

### Code Quality Tools

Must pass:
- `black` for formatting
- `flake8` for linting
- `mypy` for type checking
- `pytest` for testing (80%+ coverage)
- `bandit` for security

```bash
black backend/
flake8 backend/
mypy backend/
pytest backend/tests/ --cov=backend --cov-report=term-missing
bandit -r backend/
```

---

## API Development Guidelines

### 1. Endpoint Design

```python
# ✓ Good endpoint design
@router.post("/api/v1/tutor/ask", response_model=TutorResponse)
async def ask_question(
    request: AskQuestionRequest,
    current_user: User = Depends(get_current_user)
) -> TutorResponse:
    """Ask the tutor a question.
    
    Args:
        request: Question details
        current_user: Authenticated user
        
    Returns:
        AI tutor's response
        
    Raises:
        HTTPException: If question invalid or AI service fails
    """
    pass
```

### 2. Error Handling

```python
# Catch specific exceptions and return appropriate HTTP status
try:
    result = await tutor_service.process_question(...)
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except OpenAIError as e:
    raise HTTPException(status_code=503, detail="AI service unavailable")
```

### 3. Dependency Injection

Use FastAPI's `Depends()` for dependency injection:

```python
async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> User:
    """Extract and validate user from JWT token."""
    pass

@router.get("/api/v1/sessions")
async def list_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's sessions."""
    pass
```

### 4. Pagination

Always implement pagination for large result sets:

```python
@router.get("/api/v1/sessions", response_model=PaginatedResponse)
async def list_sessions(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user)
):
    """List sessions with pagination."""
    pass
```

---

## Service Layer Guidelines

### 1. Single Responsibility

Each service handles one domain:

```python
class TutorService:
    """Handles tutor logic."""
    async def process_question(self, ...): pass
    async def request_hint(self, ...): pass

class SessionService:
    """Handles session management."""
    async def create_session(self, ...): pass
    async def get_session(self, ...): pass
```

### 2. Dependency Management

Inject dependencies, don't instantiate them:

```python
class TutorService:
    def __init__(self, db: Session, ai_service: AIService):
        self.db = db
        self.ai_service = ai_service
    
    async def process_question(self, ...):
        response = await self.ai_service.call_openai(...)
```

### 3. Transaction Handling

Use context managers for transactions:

```python
async def create_session(self, user_id: str, topic: str):
    try:
        session = Session(user_id=user_id, topic=topic)
        self.db.add(session)
        self.db.commit()
        return session
    except Exception as e:
        self.db.rollback()
        raise
```

---

## Database Guidelines

### 1. Model Design

```python
class User(Base):
    __tablename__ = "user"
    
    user_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Relationships
    sessions: Mapped[List["Session"]] = relationship(back_populates="user")
    
    # Indexes
    __table_args__ = (
        Index("idx_email", "email"),
    )
```

### 2. Query Optimization

```python
# Use specific columns, not *
query = db.query(User.user_id, User.email)

# Eager load relationships to avoid N+1
query = db.query(User).options(selectinload(User.sessions))

# Use pagination
query = query.limit(20).offset(0)
```

### 3. Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Add user table"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

---

## Authentication Implementation

### 1. JWT Token Generation

```python
def create_access_token(user_id: str, expires_in_minutes: int = 1440) -> str:
    """Create JWT access token."""
    payload = {
        "sub": user_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
    return token
```

### 2. Token Validation

```python
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Validate token and return current user."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

---

## Testing Requirements

### 1. Unit Tests

```python
@pytest.mark.asyncio
async def test_create_user_success(user_service, db_session):
    """Test successful user creation."""
    result = await user_service.create_user(
        email="test@example.com",
        username="testuser",
        password="SecurePass123!"
    )
    assert result.email == "test@example.com"
    assert result.user_id is not None

@pytest.mark.asyncio
async def test_create_user_duplicate_email(user_service, db_session):
    """Test creation fails with duplicate email."""
    await user_service.create_user(...)
    with pytest.raises(ValueError):
        await user_service.create_user(...)
```

### 2. Integration Tests

```python
@pytest.mark.asyncio
async def test_post_question_flow(client, user_token):
    """Test complete question asking flow."""
    response = client.post(
        "/api/v1/tutor/ask",
        json={"question": "What is binary search?"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert "response" in response.json()
```

### 3. Coverage Requirements

- Minimum 80% code coverage
- All critical paths tested
- Error scenarios tested
- Edge cases covered

```bash
pytest --cov=backend --cov-report=html
```

---

## Security Checklist

- [ ] All passwords hashed (bcrypt, cost 12)
- [ ] JWT tokens validated on every request
- [ ] Input validation on all endpoints
- [ ] SQL injection protection (use ORM)
- [ ] XSS prevention (output encoding)
- [ ] CSRF tokens where needed
- [ ] Rate limiting configured
- [ ] Secrets not in code
- [ ] HTTPS enforced
- [ ] Error messages don't leak info

---

## Forbidden Practices

❌ **Never do these**:
- Hardcode secrets in code
- Log sensitive data (passwords, tokens)
- Use `eval()` or `exec()`
- Concatenate SQL queries
- Disable security features
- Use print() for logging
- Ignore security warnings
- Deploy without testing
- Use deprecated dependencies

---

## Preferred Tools & Libraries

- **Web Framework**: FastAPI
- **Async**: asyncio, httpx
- **Database**: SQLAlchemy + Alembic
- **Validation**: Pydantic
- **Testing**: pytest + pytest-asyncio
- **Linting**: Black, Flake8, MyPy
- **Security**: Bandit, python-jose
- **AI Integration**: OpenAI SDK

---

## Performance Targets

- API response time (p95): < 500ms
- Database queries (p95): < 100ms
- Throughput: > 1000 requests/second
- Uptime: 99.9%
- Error rate: < 0.1%

---

## Debugging Commands

```bash
# Check database
mysql -h localhost -u user -p thinkloop_ai

# View logs
tail -f logs/app.log

# Run tests with verbose output
pytest -vv backend/tests/

# Profile code
python -m cProfile -s cumulative app.py

# Check dependencies
pip list
pip check  # Check for conflicts
```

---

## Review Checklist

Before submitting code, verify:
- [ ] Code follows style guide
- [ ] All tests pass (80%+ coverage)
- [ ] No linting errors (black, flake8, mypy)
- [ ] Security scan passes (bandit)
- [ ] Documentation updated
- [ ] Database migrations included
- [ ] Error handling comprehensive
- [ ] No hardcoded values
- [ ] Performance acceptable
- [ ] API documented

---

**Updated**: July 2026  
**Version**: 1.0
