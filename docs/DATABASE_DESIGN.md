# Database Design Document
# thinkloop AI

**Version**: 1.0  
**Last Updated**: July 2026  
**Status**: Active

---

## 1. Entity-Relationship Diagram

```
┌──────────────┐
│     User     │
├──────────────┤
│ user_id (PK) │◄──────┐
│ email        │       │
│ username     │       │
│ password_hash│       │ 1:N
│ first_name   │       │
│ last_name    │       │
│ avatar_url   │       │
│ bio          │       │
│ role         │       │
│ is_verified  │       │
│ is_active    │       │
│ created_at   │       │
│ updated_at   │       │
│ last_login   │       │
└──────────────┘       │
       │               │
       │ 1:N           │
       ├───────────────┼──────┐
       │               │      │
       ▼               │      │
┌──────────────────────┼──┐   │
│      Session         │  │   │
├──────────────────────┤  │   │
│ session_id (PK)      │  │   │
│ user_id (FK)◄────────┘  │   │
│ topic                │  │   │
│ title                │  │   │
│ description          │  │   │
│ status               │  │   │
│ created_at           │  │   │
│ updated_at           │  │   │
│ closed_at            │  │   │
│ metadata             │  │   │
└──────────────────────┘  │   │
       │                  │   │
       │ 1:N              │   │
       ▼                  │   │
┌──────────────────────┐  │   │
│    Conversation      │  │   │
├──────────────────────┤  │   │
│ conversation_id (PK) │  │   │
│ session_id (FK)  ◄───  │   │
│ question             │  │   │
│ question_embedding   │  │   │
│ ai_response          │  │   │
│ response_time_ms     │  │   │
│ hint_level           │  │   │
│ misconception_detected
│ misconception_details│  │   │
│ user_satisfaction    │  │   │
│ created_at           │  │   │
│ updated_at           │  │   │
└──────────────────────┘  │   │
       │                  │   │
       │ 1:N              │   │
       ▼                  │   │
┌──────────────────────┐  │   │
│        Hint          │  │   │
├──────────────────────┤  │   │
│ hint_id (PK)         │  │   │
│ conversation_id (FK) │  │   │
│ level                │  │   │
│ hint_text            │  │   │
│ is_used              │  │   │
│ generated_at         │  │   │
│ used_at              │  │   │
└──────────────────────┘  │   │
                          │   │
                          │   │
│ Misconception        │   │
├──────────────────────┤   │
│ misconception_id (PK)    │
│ user_id (FK)  ◄──────────┘
│ topic
│ misconception_type
│ description
│ identified_at
│ correction_provided
│ resolved
└──────────────────────┘

┌──────────────────────┐
│   UserAnalytics      │
├──────────────────────┤
│ analytics_id (PK)    │
│ user_id (FK)  ◄──────┐
│ total_sessions       │ 1:1
│ total_questions      │
│ total_hints_used     │
│ average_session_dur. │
│ topics_covered       │
│ topics_mastered      │
│ misconceptions_id.   │
│ last_updated         │
└──────────────────────┘

┌──────────────────────┐
│   RefreshToken       │
├──────────────────────┤
│ token_id (PK)        │
│ user_id (FK)  ◄──────┐
│ token_hash           │ 1:N
│ created_at           │
│ expires_at           │
│ revoked_at           │
└──────────────────────┘
```

---

## 2. Table Definitions

### 2.1 User Table

**Purpose**: Store user account information

```sql
CREATE TABLE user (
    user_id VARCHAR(36) PRIMARY KEY COMMENT 'UUID v4',
    email VARCHAR(255) NOT NULL UNIQUE COMMENT 'User email address',
    username VARCHAR(100) NOT NULL UNIQUE COMMENT 'Username for display',
    password_hash VARCHAR(255) NOT NULL COMMENT 'Bcrypt hashed password',
    first_name VARCHAR(100) COMMENT 'First name',
    last_name VARCHAR(100) COMMENT 'Last name',
    avatar_url VARCHAR(500) COMMENT 'Profile avatar URL',
    bio TEXT COMMENT 'User biography',
    role ENUM('student', 'educator', 'admin') DEFAULT 'student' COMMENT 'User role',
    is_verified BOOLEAN DEFAULT FALSE COMMENT 'Email verified',
    is_active BOOLEAN DEFAULT TRUE COMMENT 'Account active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Account creation time',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL COMMENT 'Last login time',
    
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_role (role),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Columns**:
- `user_id`: UUID primary key, auto-generated
- `email`: Unique email address (case-insensitive)
- `username`: Display name, unique
- `password_hash`: Bcrypt hash (cost 12)
- `role`: ENUM for access control
- `is_verified`: Email verification status
- `is_active`: Soft delete flag

### 2.2 Session Table

**Purpose**: Track learning sessions

```sql
CREATE TABLE session (
    session_id VARCHAR(36) PRIMARY KEY COMMENT 'UUID v4',
    user_id VARCHAR(36) NOT NULL COMMENT 'FK to User',
    topic VARCHAR(255) COMMENT 'Learning topic',
    title VARCHAR(255) COMMENT 'Session title',
    description TEXT COMMENT 'Session description',
    status ENUM('active', 'paused', 'completed') DEFAULT 'active' COMMENT 'Session status',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    closed_at TIMESTAMP NULL COMMENT 'Session completion time',
    metadata JSON COMMENT 'Additional session metadata',
    
    CONSTRAINT fk_session_user FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_topic (topic),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_user_created (user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Columns**:
- `session_id`: UUID, primary key
- `user_id`: Foreign key to User
- `topic`: Subject area being studied
- `status`: Active/paused/completed
- `metadata`: JSON for flexible additional data

### 2.3 Conversation Table

**Purpose**: Store Q&A interactions

```sql
CREATE TABLE conversation (
    conversation_id VARCHAR(36) PRIMARY KEY COMMENT 'UUID v4',
    session_id VARCHAR(36) NOT NULL COMMENT 'FK to Session',
    question TEXT NOT NULL COMMENT 'Student question',
    question_embedding LONGBLOB COMMENT 'Vector embedding for similarity search',
    ai_response TEXT COMMENT 'AI-generated response',
    response_time_ms INT COMMENT 'Response generation time',
    hint_level INT DEFAULT 0 COMMENT 'Current hint level (0-6)',
    misconception_detected BOOLEAN DEFAULT FALSE,
    misconception_details JSON COMMENT 'Details of misconception if detected',
    user_satisfaction INT COMMENT 'User rating 1-5 for response quality',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_conversation_session FOREIGN KEY (session_id) REFERENCES session(session_id) ON DELETE CASCADE,
    
    INDEX idx_session_id (session_id),
    INDEX idx_created_at (created_at),
    INDEX idx_misconception (misconception_detected),
    FULLTEXT INDEX ft_question (question)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Columns**:
- `conversation_id`: UUID, primary key
- `session_id`: Foreign key to Session
- `question`: Full text of student question
- `ai_response`: Generated response text
- `response_time_ms`: Track AI response latency
- `hint_level`: Track which hint level is active (0=question, 6=full answer)
- `misconception_details`: JSON with misconception analysis
- `user_satisfaction`: 1-5 rating

### 2.4 Hint Table

**Purpose**: Store hint records

```sql
CREATE TABLE hint (
    hint_id VARCHAR(36) PRIMARY KEY COMMENT 'UUID v4',
    conversation_id VARCHAR(36) NOT NULL COMMENT 'FK to Conversation',
    level INT NOT NULL COMMENT 'Hint level 1-6',
    hint_text TEXT NOT NULL COMMENT 'Hint content',
    is_used BOOLEAN DEFAULT FALSE COMMENT 'Whether hint was shown',
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    used_at TIMESTAMP NULL COMMENT 'When hint was displayed',
    
    CONSTRAINT fk_hint_conversation FOREIGN KEY (conversation_id) REFERENCES conversation(conversation_id) ON DELETE CASCADE,
    CONSTRAINT chk_hint_level CHECK (level >= 1 AND level <= 6),
    
    INDEX idx_conversation_id (conversation_id),
    INDEX idx_level (level),
    INDEX idx_is_used (is_used)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Columns**:
- `hint_id`: UUID, primary key
- `level`: 1-6 indicating hint specificity
- `is_used`: Whether hint was shown to student
- `used_at`: Timestamp when hint was displayed

### 2.5 UserAnalytics Table

**Purpose**: Track user learning metrics

```sql
CREATE TABLE user_analytics (
    analytics_id VARCHAR(36) PRIMARY KEY COMMENT 'UUID v4',
    user_id VARCHAR(36) NOT NULL UNIQUE COMMENT 'FK to User (1:1)',
    total_sessions INT DEFAULT 0 COMMENT 'Total learning sessions',
    total_questions INT DEFAULT 0 COMMENT 'Total questions asked',
    total_hints_used INT DEFAULT 0 COMMENT 'Total hints requested',
    average_session_duration_min FLOAT DEFAULT 0 COMMENT 'Average session duration in minutes',
    topics_covered JSON COMMENT 'Array of topics studied',
    topics_mastered JSON COMMENT 'Array of mastered topics',
    misconceptions_identified INT DEFAULT 0 COMMENT 'Total misconceptions detected',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_analytics_user FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_last_updated (last_updated)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Columns**:
- `analytics_id`: UUID, primary key
- `user_id`: Foreign key to User (1:1 relationship)
- All metrics are aggregates updated periodically
- `topics_covered` and `topics_mastered` are JSON arrays

### 2.6 Misconception Table

**Purpose**: Track identified misconceptions

```sql
CREATE TABLE misconception (
    misconception_id VARCHAR(36) PRIMARY KEY COMMENT 'UUID v4',
    user_id VARCHAR(36) NOT NULL COMMENT 'FK to User',
    topic VARCHAR(255) NOT NULL COMMENT 'Topic of misconception',
    misconception_type VARCHAR(100) COMMENT 'Category of misconception',
    description TEXT COMMENT 'Detailed description of misconception',
    identified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    correction_provided BOOLEAN DEFAULT FALSE COMMENT 'Whether correction was given',
    resolved BOOLEAN DEFAULT FALSE COMMENT 'Whether misconception is resolved',
    resolved_at TIMESTAMP NULL,
    
    CONSTRAINT fk_misconception_user FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_topic (topic),
    INDEX idx_resolved (resolved),
    INDEX idx_identified_at (identified_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 2.7 RefreshToken Table

**Purpose**: Manage refresh token lifecycle

```sql
CREATE TABLE refresh_token (
    token_id VARCHAR(36) PRIMARY KEY COMMENT 'UUID v4',
    user_id VARCHAR(36) NOT NULL COMMENT 'FK to User',
    token_hash VARCHAR(255) NOT NULL UNIQUE COMMENT 'SHA256 hash of token',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL COMMENT 'Token expiration time',
    revoked_at TIMESTAMP NULL COMMENT 'Revocation time if revoked',
    
    CONSTRAINT fk_refresh_token_user FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_token_hash (token_hash),
    INDEX idx_expires_at (expires_at),
    INDEX idx_revoked_at (revoked_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 3. Relationships & Constraints

### 3.1 Foreign Key Relationships

| Relationship | Parent | Child | Constraint | On Delete |
|-------------|--------|-------|-----------|-----------|
| User → Session | User | Session | 1:N | CASCADE |
| User → Misconception | User | Misconception | 1:N | CASCADE |
| User → RefreshToken | User | RefreshToken | 1:N | CASCADE |
| User → UserAnalytics | User | UserAnalytics | 1:1 | CASCADE |
| Session → Conversation | Session | Conversation | 1:N | CASCADE |
| Conversation → Hint | Conversation | Hint | 1:N | CASCADE |

### 3.2 Constraints

**Data Integrity**:
- `user.email`: UNIQUE, NOT NULL
- `user.username`: UNIQUE, NOT NULL
- `user.password_hash`: NOT NULL, bcrypt format
- `session.user_id`: NOT NULL, FK
- `conversation.session_id`: NOT NULL, FK
- `hint.level`: CHECK (1 ≤ level ≤ 6)
- `misconception_identified`: BOOLEAN, cannot be NULL

**Temporal Constraints**:
- `closed_at` ≥ `created_at`
- `resolved_at` ≥ `identified_at` (if not NULL)
- `revoked_at` ≥ `created_at` (if not NULL)
- `used_at` ≥ `generated_at` (if not NULL)

---

## 4. Indexing Strategy

### 4.1 Primary Indexes

```sql
-- User table indexes
INDEX idx_email (email)  -- For login queries
INDEX idx_created_at (created_at)  -- For analytics

-- Session table indexes
INDEX idx_user_id (user_id)  -- FK lookup
INDEX idx_user_created (user_id, created_at)  -- User sessions ordered by date
INDEX idx_topic (topic)  -- Filter by topic
INDEX idx_status (status)  -- Filter by status

-- Conversation table indexes
INDEX idx_session_id (session_id)  -- FK lookup
INDEX idx_created_at (created_at)  -- Temporal queries
INDEX idx_misconception (misconception_detected)  -- Find misconceptions

-- Hint table indexes
INDEX idx_conversation_id (conversation_id)  -- FK lookup
INDEX idx_level (level)  -- Filter by hint level

-- Analytics table indexes
INDEX idx_user_id (user_id)  -- User lookup

-- Refresh token indexes
INDEX idx_user_id (user_id)  -- Find tokens for user
INDEX idx_expires_at (expires_at)  -- Find expired tokens
```

### 4.2 Full-Text Indexes

```sql
-- Conversation table
FULLTEXT INDEX ft_question (question)  -- Full-text search on questions
```

### 4.3 Composite Indexes

```sql
-- Session queries for a user ordered by creation
INDEX idx_user_created (user_id, created_at)

-- Refresh token queries
INDEX idx_token_hash (token_hash)  -- For token validation
```

---

## 5. Query Patterns & Optimization

### 5.1 Common Queries

**Find user sessions**:
```sql
SELECT * FROM session 
WHERE user_id = ? AND status = 'active' 
ORDER BY created_at DESC 
LIMIT 10;
```
**Index Used**: idx_user_created

**Get conversation history**:
```sql
SELECT * FROM conversation 
WHERE session_id = ? 
ORDER BY created_at ASC 
LIMIT 100 OFFSET ?;
```
**Index Used**: idx_session_id

**Find misconceptions**:
```sql
SELECT * FROM misconception 
WHERE user_id = ? AND resolved = FALSE 
ORDER BY identified_at DESC;
```
**Index Used**: idx_user_id, idx_resolved

**Get user by email**:
```sql
SELECT * FROM user WHERE email = ?;
```
**Index Used**: idx_email

### 5.2 Query Optimization Tips

1. **Use Pagination**: Always use LIMIT/OFFSET for large result sets
2. **Selective Columns**: SELECT only needed columns, not *
3. **Filter Early**: Apply WHERE clauses before JOINs
4. **Use Indexes**: Verify EXPLAIN shows index usage
5. **Avoid Subqueries**: Use JOINs instead when possible
6. **Denormalization**: UserAnalytics table denormalizes for fast dashboard queries

---

## 6. Normalization

### 6.1 Normal Forms

**First Normal Form (1NF)**: ✓
- All columns contain atomic values
- No repeating groups

**Second Normal Form (2NF)**: ✓
- Meets 1NF
- All non-key columns depend on entire primary key

**Third Normal Form (3NF)**: ✓
- Meets 2NF
- No transitive dependencies
- Non-key columns depend only on primary key

**Exceptions**:
- `UserAnalytics` denormalizes aggregate data for performance
- `metadata` JSON field allows flexible schema

---

## 7. Data Seeding & Migration

### 7.1 Alembic Migrations

Initial migration creates all tables:

```
alembic/versions/001_create_initial_schema.py
```

**Migration Order**:
1. User table (no dependencies)
2. Session table (depends on User)
3. Conversation table (depends on Session)
4. Hint table (depends on Conversation)
5. UserAnalytics table (depends on User)
6. Misconception table (depends on User)
7. RefreshToken table (depends on User)

### 7.2 Seed Data

```python
# Create initial admin user
admin = User(
    user_id=uuid.uuid4(),
    email='admin@thinkloop.ai',
    username='admin',
    password_hash=hash_password('admin_password'),
    role='admin',
    is_verified=True,
    is_active=True
)

# Create demo student user
student = User(
    user_id=uuid.uuid4(),
    email='demo@thinkloop.ai',
    username='demo_student',
    password_hash=hash_password('demo_password'),
    role='student',
    is_verified=True,
    is_active=True
)
```

---

## 8. Backup & Recovery

### 8.1 Backup Strategy

- **Frequency**: Daily automated snapshots
- **Retention**: 35 days
- **Redundancy**: Multi-AZ replication
- **Recovery**: Point-in-time recovery

### 8.2 Recovery Procedures

**Full database recovery**:
```bash
# Create RDS snapshot
aws rds create-db-snapshot --db-instance-identifier thinkloop-prod --db-snapshot-identifier thinkloop-recovery-20260723

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier thinkloop-prod-recovered \
  --db-snapshot-identifier thinkloop-recovery-20260723
```

---

## 9. Performance Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Query Response Time (p95) | <100ms | - |
| Table Size (GB) | <50GB (Y1) | - |
| Index Size (GB) | <10GB | - |
| Query Count/sec | <1000 | - |
| Write IOPS | 5000 | - |
| Read IOPS | 20000 | - |

---

## 10. Conclusion

This database schema provides:
- **Normalization**: Efficient data storage
- **Scalability**: Optimized for growth
- **Integrity**: Strong constraints
- **Performance**: Strategic indexing
- **Flexibility**: JSON fields for extensibility
- **Auditability**: Temporal columns for tracking

---

**Document Owner**: Database Architect  
**Last Updated**: July 2026
