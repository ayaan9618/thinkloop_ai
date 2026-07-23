# System Design Document
# thinkloop AI

## Document Information

**Version**: 1.0  
**Last Updated**: July 2026  
**Author**: Architecture Team  
**Status**: Active

---

## 1. Architecture Overview

### High-Level Architecture

```
                    ┌─────────────────────────────────┐
                    │   Client Layer (Frontend)       │
                    │  HTML5 + Tailwind + Vanilla JS  │
                    └────────────┬────────────────────┘
                                 │
                                 │ HTTPS/TLS 1.3
                                 │
        ┌────────────────────────▼────────────────────────┐
        │  AWS Elastic Beanstalk (Application Tier)      │
        │                                                 │
        │  ┌─────────────────────────────────────────┐   │
        │  │    FastAPI + Uvicorn (Python)          │   │
        │  │  • Request Handler                      │   │
        │  │  • Rate Limiting                        │   │
        │  │  • Error Handling                       │   │
        │  │  • CORS Management                      │   │
        │  └─────────────────────────────────────────┘   │
        │                                                 │
        │  ┌─────────────────────────────────────────┐   │
        │  │    Authentication Service               │   │
        │  │  • JWT Token Generation                 │   │
        │  │  • OAuth2 Provider Integration          │   │
        │  │  • Session Management                   │   │
        │  │  • Password Hashing (bcrypt)            │   │
        │  └─────────────────────────────────────────┘   │
        │                                                 │
        │  ┌─────────────────────────────────────────┐   │
        │  │    AI/Tutor Service                     │   │
        │  │  • Prompt Engineering                   │   │
        │  │  • Hint Generation                      │   │
        │  │  • Misconception Detection              │   │
        │  │  • Conversation Context Management      │   │
        │  └─────────────────────────────────────────┘   │
        │                                                 │
        │  ┌─────────────────────────────────────────┐   │
        │  │    Business Logic Layer                 │   │
        │  │  • Session Management                   │   │
        │  │  • Analytics Processing                 │   │
        │  │  • User Management                      │   │
        │  │  • Content Management                   │   │
        │  └─────────────────────────────────────────┘   │
        │                                                 │
        │  ┌─────────────────────────────────────────┐   │
        │  │    Data Access Layer (SQLAlchemy)       │   │
        │  │  • ORM Mapping                          │   │
        │  │  • Query Optimization                   │   │
        │  │  • Connection Pooling                   │   │
        │  └─────────────────────────────────────────┘   │
        └────────────────┬───────────────┬────────────────┘
                         │               │
        ┌────────────────▼──┐  ┌────────▼──────────────┐
        │  AWS RDS MySQL    │  │  AWS Services        │
        │  • User Data      │  │  • Secrets Manager   │
        │  • Sessions       │  │  • CloudWatch        │
        │  • Conversations  │  │  • IAM               │
        │  • Analytics      │  │  • Route 53          │
        └────────────────────┘  └─────────────────────┘

        ┌────────────────────────────────────┐
        │     External Services              │
        │  • OpenAI API (GPT-4, GPT-3.5)    │
        │  • OAuth2 Providers                │
        │  • Email Service (AWS SES)         │
        └────────────────────────────────────┘
```

### Technology Layers

#### 1. Presentation Layer
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript (ES6)
- **Protocol**: HTTPS/REST
- **Served**: Static assets via CloudFront CDN

#### 2. Application Layer
- **Runtime**: Python 3.10+
- **Web Framework**: FastAPI
- **ASGI Server**: Uvicorn
- **Data Validation**: Pydantic
- **Hosting**: AWS Elastic Beanstalk

#### 3. Business Logic Layer
- Authentication Service
- AI/Tutor Service
- Session Management Service
- Analytics Service
- Content Management Service

#### 4. Data Access Layer
- **ORM**: SQLAlchemy
- **Database Driver**: PyMySQL
- **Connection Pooling**: SQLAlchemy Pool
- **Migrations**: Alembic

#### 5. Data Storage Layer
- **Primary Database**: AWS RDS MySQL 8.0
- **Session Cache**: Redis (planned)
- **Document Storage**: S3 (for exports)

---

## 2. Component Architecture

### Core Components

#### 2.1 Authentication Component

**Responsibilities**:
- User registration and login
- JWT token generation and validation
- OAuth2 provider integration
- Session management
- Password hashing and verification

**Key Classes**:
```
auth_service.py
├── AuthService
│   ├── register_user()
│   ├── login_user()
│   ├── refresh_token()
│   ├── validate_token()
│   └── logout_user()
│
jwt_utils.py
├── JWTManager
│   ├── create_token()
│   ├── decode_token()
│   └── refresh_token()
│
oauth_provider.py
├── OAuthProvider
│   ├── get_google_token()
│   ├── get_github_token()
│   └── get_microsoft_token()
```

**Data Models**:
- `User`: User account information
- `Session`: Active sessions
- `RefreshToken`: Refresh token tracking

#### 2.2 Tutor Service Component

**Responsibilities**:
- Process user questions
- Generate Socratic responses
- Manage hint escalation
- Detect misconceptions
- Provide complete answers

**Key Classes**:
```
tutor_service.py
├── TutorService
│   ├── process_question()
│   ├── generate_response()
│   ├── request_hint()
│   ├── reveal_answer()
│   └── get_debug_help()
│
ai_service.py
├── AIService
│   ├── call_openai()
│   ├── format_prompt()
│   ├── validate_response()
│   └── handle_error()
│
prompt_manager.py
├── PromptManager
│   ├── get_tutor_prompt()
│   ├── get_hint_prompt()
│   ├── get_detection_prompt()
│   └── format_context()
│
misconception_detector.py
├── MisconceptionDetector
│   ├── detect()
│   ├── analyze_response()
│   └── suggest_correction()
```

**Data Models**:
- `Conversation`: Question-response pairs
- `Hint`: Hint records with levels
- `Misconception`: Detected misconceptions
- `ConversationContext`: Conversation history

#### 2.3 Session Management Component

**Responsibilities**:
- Create and manage user sessions
- Track conversation history
- Maintain session state
- Handle session resumption

**Key Classes**:
```
session_service.py
├── SessionService
│   ├── create_session()
│   ├── get_session()
│   ├── update_session()
│   ├── close_session()
│   └── resume_session()
│
session_store.py
├── SessionStore
│   ├── save()
│   ├── load()
│   ├── delete()
│   └── query()
```

**Data Models**:
- `Session`: Session metadata
- `Interaction`: Individual question-response

#### 2.4 Analytics Component

**Responsibilities**:
- Track learning progress
- Generate analytics reports
- Calculate learning insights
- Process usage metrics

**Key Classes**:
```
analytics_service.py
├── AnalyticsService
│   ├── track_interaction()
│   ├── calculate_progress()
│   ├── get_insights()
│   ├── get_statistics()
│   └── export_report()
│
metrics.py
├── Metrics
│   ├── session_duration
│   ├── hints_requested
│   ├── accuracy_rate
│   └── topics_covered
```

**Data Models**:
- `UserAnalytics`: User-level metrics
- `SessionMetrics`: Session-level metrics
- `TopicProgress`: Topic mastery tracking

---

## 3. Request Flow Diagrams

### 3.1 User Registration Flow

```
User Input (HTML Form)
        │
        ▼
Frontend JavaScript
├─ Validate input
├─ Hash password (client-side salt)
└─ POST /api/v1/auth/register
        │
        ▼
FastAPI Route Handler
├─ Validate request
├─ Check email uniqueness
├─ Validate password strength
└─ Call AuthService.register_user()
        │
        ▼
AuthService
├─ Hash password (bcrypt)
├─ Create User object
├─ Save to database
└─ Send verification email
        │
        ▼
Database (RDS MySQL)
└─ User record created
        │
        ▼
Email Service (AWS SES)
└─ Verification email sent
        │
        ▼
Response to Client
├─ 201 Created
├─ Redirect to verify email page
└─ Store temporary session token
```

### 3.2 Question Asking Flow

```
User Asks Question (Frontend UI)
        │
        ▼
Frontend JavaScript
├─ Validate input
├─ Show loading state
└─ POST /api/v1/tutor/ask
        │
        ▼
FastAPI Route Handler
├─ Authenticate (JWT)
├─ Validate request
└─ Call TutorService.process_question()
        │
        ▼
TutorService
├─ Load current session
├─ Retrieve conversation history
├─ Call AIService.generate_response()
└─ Save interaction to database
        │
        ▼
AIService
├─ Build context from history
├─ Format prompt using PromptManager
├─ Call OpenAI API
├─ Validate response
└─ Detect misconceptions if any
        │
        ▼
OpenAI API (GPT-4/GPT-3.5)
└─ Generate Socratic response
        │
        ▼
MisconceptionDetector (if flagged)
├─ Analyze student response
├─ Identify gaps
└─ Suggest targeted guidance
        │
        ▼
Response to Frontend
├─ 200 OK with response
├─ Include conversation_id
├─ Include response_id
└─ Include hint availability
        │
        ▼
Frontend Updates UI
├─ Display AI response
├─ Show hint button
├─ Enable next question input
└─ Save interaction locally
```

### 3.3 Hint Request Flow

```
User Requests Hint (Frontend)
        │
        ▼
Frontend JavaScript
├─ Check hint level
├─ Validate hint availability
└─ POST /api/v1/tutor/hint
        │
        ▼
FastAPI Route Handler
├─ Authenticate (JWT)
├─ Validate hint request
└─ Call TutorService.request_hint()
        │
        ▼
TutorService
├─ Load conversation context
├─ Get current hint level
├─ Call AIService.generate_hint()
├─ Increment hint counter
└─ Save hint record
        │
        ▼
AIService
├─ Get hint template for level
├─ Format prompt with context
├─ Call OpenAI API
└─ Validate hint quality
        │
        ▼
Response to Frontend
├─ 200 OK with hint
├─ Include updated hint_level
├─ Include remaining hints (if quota)
└─ Display hint progressively
```

### 3.4 Authentication Flow

```
User Login (HTML Form)
        │
        ▼
Frontend JavaScript
├─ Validate email/password
└─ POST /api/v1/auth/login
        │
        ▼
FastAPI Route Handler
├─ Validate request format
└─ Call AuthService.login_user()
        │
        ▼
AuthService
├─ Query User by email
├─ Verify password (bcrypt)
├─ Call JWTManager.create_token()
├─ Create RefreshToken record
└─ Update user last_login
        │
        ▼
JWTManager
├─ Create JWT payload (user_id, exp, iat)
├─ Sign with HS256
└─ Return token
        │
        ▼
Response to Frontend
├─ 200 OK
├─ Return JWT token
├─ Return refresh token
├─ Return user profile
└─ Set secure HTTP-only cookie
        │
        ▼
Frontend
├─ Store JWT in memory/session storage
├─ Store refresh token in HTTP-only cookie
└─ Redirect to dashboard
```

### 3.5 OAuth2 Flow

```
User Clicks "Login with Google"
        │
        ▼
Frontend
└─ Redirect to Google OAuth endpoint
        │
        ▼
Google OAuth Provider
├─ User authenticates
└─ Return authorization code + state
        │
        ▼
Frontend
└─ POST /api/v1/auth/oauth/callback
        │
        ▼
FastAPI Route Handler
├─ Validate state parameter
├─ Exchange code for Google access token
└─ Call OAuthProvider.verify_google_token()
        │
        ▼
OAuthProvider
├─ Call Google API to get user info
├─ Check if user exists in database
├─ Create new user if needed
├─ Call JWTManager.create_token()
└─ Return JWT + refresh token
        │
        ▼
Response to Frontend
├─ 200 OK
├─ Return JWT token
├─ Return refresh token
└─ Redirect to dashboard
```

---

## 4. Database Design Overview

### Data Model

```
User (PK: user_id)
├─ user_id: UUID
├─ email: String (unique)
├─ username: String
├─ password_hash: String
├─ first_name: String
├─ last_name: String
├─ avatar_url: String
├─ bio: Text
├─ role: Enum (student, educator, admin)
├─ is_verified: Boolean
├─ is_active: Boolean
├─ created_at: DateTime
├─ updated_at: DateTime
└─ last_login: DateTime

Session (PK: session_id, FK: user_id)
├─ session_id: UUID
├─ user_id: UUID (FK)
├─ topic: String
├─ title: String
├─ description: Text
├─ status: Enum (active, paused, completed)
├─ created_at: DateTime
├─ updated_at: DateTime
├─ closed_at: DateTime
└─ metadata: JSON

Conversation (PK: conversation_id, FK: session_id)
├─ conversation_id: UUID
├─ session_id: UUID (FK)
├─ question: Text
├─ question_embedding: Vector (optional)
├─ ai_response: Text
├─ response_time_ms: Integer
├─ hint_level: Integer
├─ misconception_detected: Boolean
├─ misconception_details: JSON
├─ user_satisfaction: Integer (1-5)
├─ created_at: DateTime
└─ updated_at: DateTime

Hint (PK: hint_id, FK: conversation_id)
├─ hint_id: UUID
├─ conversation_id: UUID (FK)
├─ level: Integer (1-6)
├─ hint_text: Text
├─ is_used: Boolean
├─ generated_at: DateTime
└─ used_at: DateTime

UserAnalytics (PK: analytics_id, FK: user_id)
├─ analytics_id: UUID
├─ user_id: UUID (FK)
├─ total_sessions: Integer
├─ total_questions: Integer
├─ total_hints_used: Integer
├─ average_session_duration: Float
├─ topics_covered: JSON
├─ topics_mastered: JSON
├─ misconceptions_identified: Integer
├─ last_updated: DateTime
└─ updated_at: DateTime

Misconception (PK: misconception_id)
├─ misconception_id: UUID
├─ user_id: UUID (FK)
├─ topic: String
├─ misconception_type: String
├─ description: Text
├─ identified_at: DateTime
├─ correction_provided: Boolean
└─ resolved: Boolean

RefreshToken (PK: token_id, FK: user_id)
├─ token_id: UUID
├─ user_id: UUID (FK)
├─ token_hash: String (hashed)
├─ created_at: DateTime
├─ expires_at: DateTime
└─ revoked_at: DateTime (nullable)
```

### Relationships

```
User (1) ──── (N) Session
User (1) ──── (N) Misconception
User (1) ──── (N) RefreshToken
User (1) ──── (1) UserAnalytics

Session (1) ──── (N) Conversation
Conversation (1) ──── (N) Hint
```

---

## 5. AI/LLM Integration Flow

### 5.1 Prompt Engineering Strategy

**Hierarchical Prompt Structure**:

```
┌─ System Prompt (Master Instructions)
│  ├─ Behavior Definition
│  ├─ Teaching Philosophy
│  ├─ Safety Guidelines
│  └─ Output Formatting
│
├─ Few-Shot Examples
│  ├─ Example 1: Good Question Response
│  ├─ Example 2: Hint Generation
│  └─ Example 3: Misconception Correction
│
├─ Context (Conversation History)
│  ├─ Previous questions
│  ├─ Previous responses
│  ├─ Student knowledge level
│  └─ Current topic
│
└─ User Input (Current Question)
   └─ Student's actual question
```

### 5.2 Response Validation Pipeline

```
OpenAI API Response
        │
        ▼
Syntax Validation
├─ Check JSON format (if structured)
├─ Verify response length
└─ Check for required fields
        │
        ▼
Content Validation
├─ Check for harmful content
├─ Verify educational value
├─ Check for toxicity
└─ Validate against guidelines
        │
        ▼
Quality Scoring
├─ Relevance score
├─ Coherence score
├─ Pedagogical appropriateness
└─ Length appropriateness
        │
        ▼
Misconception Analysis
├─ Identify incorrect patterns
├─ Flag for correction
└─ Suggest alternative explanations
        │
        ▼
Final Response
├─ Pass to client if quality > threshold
├─ Regenerate if quality < threshold
└─ Escalate to human review if confidence low
```

---

## 6. Security Architecture

### 6.1 Authentication & Authorization

**Authentication Flow**:
1. User provides credentials (email/password or OAuth)
2. Server validates credentials
3. JWT token issued (24-hour expiration)
4. Client includes JWT in Authorization header
5. Server validates JWT on each request

**JWT Token Structure**:
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id",
    "email": "user@example.com",
    "role": "student",
    "iat": 1719115200,
    "exp": 1719201600
  },
  "signature": "HMACSHA256(base64UrlEncode(header) + '.' + base64UrlEncode(payload), secret)"
}
```

### 6.2 Data Protection

**Encryption In Transit**:
- HTTPS/TLS 1.3 for all connections
- Certificate managed by AWS Certificate Manager
- HSTS enabled (31536000 seconds)

**Encryption At Rest**:
- Database: MySQL native encryption or AWS RDS encryption
- Sensitive fields hashed: passwords (bcrypt), API keys
- PII masked in logs

**Password Security**:
- Bcrypt with salt rounds: 12
- Minimum requirements: 8 chars, mixed case, numbers, symbols
- Password reset token: 32-byte random, 1-hour expiration
- Constant-time comparison for password verification

### 6.3 API Security

**Rate Limiting**:
- Global: 10,000 requests/minute per IP
- Per-user: 100 requests/minute
- Per-endpoint: Configurable limits
- Sliding window algorithm
- Response includes `X-RateLimit-*` headers

**Input Validation**:
- All inputs validated against Pydantic schemas
- SQL injection prevention via SQLAlchemy ORM
- XSS prevention via response sanitization
- CSRF protection via CSRF tokens

**CORS Configuration**:
- Allow only approved origins (configurable)
- Expose only necessary headers
- Credentials included in cross-origin requests
- Preflight requests handled correctly

### 6.4 Infrastructure Security

**Network Security**:
- VPC with private subnets for RDS
- Security groups restricting inbound/outbound
- VPC endpoints for AWS services
- NACLs for additional network control

**Access Control**:
- IAM roles for Elastic Beanstalk
- Principle of least privilege
- Service-to-service authentication via IAM
- Secrets Manager for API keys rotation

**Monitoring & Alerting**:
- CloudWatch Logs for all API calls
- CloudWatch Alarms for suspicious activity
- VPC Flow Logs for network traffic
- GuardDuty for threat detection

---

## 7. Scalability Strategy

### 7.1 Horizontal Scaling

**Application Layer**:
- Auto Scaling Group in Elastic Beanstalk
- Min: 2 instances, Max: 20 instances
- Scale based on CPU utilization (70% threshold) or request count
- Rolling deployments for zero-downtime updates

**Database Layer**:
- Read replicas for scaling read operations
- Connection pooling (SQLAlchemy): 5-20 connections per instance
- Query optimization and indexing
- Partitioning for large tables if needed

### 7.2 Caching Strategy

**Application Cache (Redis)**:
- Session tokens
- Frequently accessed user profiles
- Prompt templates
- Generated responses (temporary)
- Cache invalidation on updates

**CDN Cache (CloudFront)**:
- Static assets (HTML, CSS, JS)
- Images and icons
- API responses with Cache-Control headers

### 7.3 Load Balancing

**AWS Elastic Load Balancer**:
- Application Load Balancer (ALB)
- Health checks every 30 seconds
- Connection draining: 300 seconds
- Sticky sessions: Disabled (stateless design)

### 7.4 Performance Optimizations

**Database Optimizations**:
- Indexes on frequently queried columns (user_id, session_id, created_at)
- Query optimization and pagination (limit 100 per page)
- Connection pooling to reduce overhead

**API Optimizations**:
- Response compression (gzip)
- Pagination for large result sets
- Lazy loading of related objects
- GraphQL queries (future consideration)

**Frontend Optimizations**:
- Minified and bundled CSS/JS
- Lazy loading of images
- Service Worker for offline caching
- Debouncing/throttling for API calls

---

## 8. Monitoring, Logging & Observability

### 8.1 Logging Strategy

**Application Logs**:
```json
{
  "timestamp": "2026-07-23T10:30:45Z",
  "level": "INFO",
  "logger": "app.services.tutor_service",
  "message": "Question processed successfully",
  "request_id": "req-123-456",
  "user_id": "user-789",
  "session_id": "session-234",
  "duration_ms": 245,
  "trace_id": "trace-567"
}
```

**Log Levels**:
- DEBUG: Development debugging information
- INFO: General informational messages
- WARNING: Warning conditions
- ERROR: Error conditions
- CRITICAL: Critical errors requiring immediate attention

**Log Retention**:
- CloudWatch Logs: 30 days default
- Archive to S3: Logs older than 30 days
- S3 Glacier: Logs older than 90 days

### 8.2 Metrics & Monitoring

**Key Metrics**:

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| API Response Time (p95) | <500ms | >1000ms |
| Error Rate | <0.1% | >1% |
| CPU Utilization | 50-70% | >85% |
| Memory Utilization | 60-80% | >90% |
| Database Connections | <80% of max | >90% |
| Database Query Time (p95) | <100ms | >500ms |
| OpenAI API Latency | <5s | >10s |
| Session Success Rate | >95% | <90% |

**CloudWatch Dashboards**:
- Application Health Dashboard
- Performance Dashboard
- Error and Exception Dashboard
- Business Metrics Dashboard

### 8.3 Distributed Tracing

**Trace Structure**:
```
Request comes in
  ├─ Generate trace_id
  ├─ Authenticate user (span)
  │  ├─ Query database (span)
  │  └─ Validate token (span)
  ├─ Process tutor request (span)
  │  ├─ Call OpenAI API (span)
  │  ├─ Detect misconception (span)
  │  └─ Save to database (span)
  └─ Send response (span)
```

**Trace Context Propagation**:
- X-Trace-ID header
- Passed to OpenAI API
- Included in database queries
- Logged in all events

---

## 9. Disaster Recovery & Business Continuity

### 9.1 Backup Strategy

**Database Backups**:
- Automated daily snapshots (AWS RDS)
- Point-in-time recovery: 7 days
- Backup retention: 35 days
- Multi-AZ replication

**Application Backups**:
- Source code in GitHub (version controlled)
- Terraform/CloudFormation templates in GitHub
- Configuration in Secrets Manager
- Database migrations in version control

### 9.2 Disaster Recovery Plan

**RTO (Recovery Time Objective)**: < 4 hours  
**RPO (Recovery Point Objective)**: < 1 hour

**Failure Scenarios**:

1. **Single Instance Failure**
   - Auto Scaling Group replaces failed instance
   - RTO: < 5 minutes
   - No data loss

2. **Database Failure**
   - Failover to multi-AZ replica
   - RTO: < 5 minutes
   - No data loss

3. **Region Failure**
   - Manual failover to secondary region (not automatic)
   - RTO: < 4 hours
   - Data loss: < 1 hour

4. **Data Corruption**
   - Restore from previous snapshot
   - RTO: < 1 hour
   - RPO: < 1 day

### 9.3 Health Checks

**Application Health Checks**:
```
GET /health
{
  "status": "healthy",
  "timestamp": "2026-07-23T10:30:45Z",
  "database": "connected",
  "openai_api": "available",
  "version": "1.0.0"
}
```

---

## 10. Deployment Architecture

### 10.1 Deployment Pipeline

```
GitHub Push
  │
  ▼
GitHub Actions CI
├─ Run tests
├─ Run linting
├─ Build artifacts
└─ Run security scanning
  │
  ▼
Approval Gate (if production)
  │
  ▼
AWS CodeDeploy
├─ Pull artifacts from S3
├─ Stop old application
├─ Deploy new application
├─ Run health checks
└─ Update load balancer
  │
  ▼
Smoke Tests
├─ Verify endpoints responding
├─ Check database connectivity
└─ Validate critical flows
  │
  ▼
Deployment Complete
```

### 10.2 Environment Configurations

| Environment | Purpose | Scale | Monitoring |
|-------------|---------|-------|-----------|
| Development | Local development | Single instance | Basic |
| Staging | Pre-production testing | 2-4 instances | Standard |
| Production | Live traffic | 4-20 instances | Enhanced |

---

## 11. Conclusion

This system design provides a scalable, secure, and maintainable architecture for thinkloop AI. The design follows cloud-native best practices, emphasizes security, and enables rapid iteration and scaling.

Key design decisions:
- Stateless application layer for horizontal scaling
- FastAPI for high performance
- MySQL for reliable data persistence
- AWS managed services for reliability
- Comprehensive monitoring and logging
- Security-first approach
- Clear separation of concerns

---

**Document Owner**: Architecture Team  
**Last Updated**: July 2026  
**Next Review**: August 2026
