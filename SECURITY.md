# Security Policy & Guidelines
# thinkloop AI

**Version**: 1.0  
**Last Updated**: July 2026  
**Status**: Active

---

## Table of Contents

1. [Security Overview](#security-overview)
2. [Authentication & Authorization](#authentication--authorization)
3. [Data Protection](#data-protection)
4. [API Security](#api-security)
5. [Vulnerability Disclosure](#vulnerability-disclosure)
6. [Security Best Practices](#security-best-practices)
7. [Compliance](#compliance)
8. [Incident Response](#incident-response)

---

## Security Overview

Security is a core concern in thinkloop AI. We implement defense-in-depth with multiple layers of protection.

### Security Principles

1. **Least Privilege**: Users have only necessary permissions
2. **Defense in Depth**: Multiple security layers
3. **Secure by Default**: Security is enabled by default
4. **Regular Auditing**: Continuous security monitoring
5. **Transparency**: Clear security policies
6. **Rapid Response**: Quick vulnerability patching

---

## Authentication & Authorization

### 1. User Authentication

#### JWT Tokens

- **Algorithm**: HS256 (HMAC SHA-256)
- **Expiration**: 24 hours for access tokens
- **Refresh Tokens**: 30-day validity
- **Storage**: Access tokens in memory/localStorage, refresh tokens in HTTP-only cookies
- **Validation**: Every API request validates JWT signature

```python
# JWT Structure
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id",        # Subject (user)
    "email": "user@example.com",
    "role": "student",
    "iat": 1719115200,       # Issued at
    "exp": 1719201600        # Expires at
  },
  "signature": "HMACSHA256(header.payload, secret)"
}
```

#### Password Requirements

- **Minimum Length**: 8 characters
- **Complexity**: Must contain:
  - Uppercase letters (A-Z)
  - Lowercase letters (a-z)
  - Numbers (0-9)
  - Special characters (!@#$%^&*)
- **Hashing**: Bcrypt with 12 salt rounds
- **Storage**: Never stored in plain text

#### Password Reset

- **Token Validity**: 1 hour
- **Token Type**: Cryptographically random 32-byte token
- **One-Time Use**: Token invalidated after use
- **Verification**: Email verification required

### 2. OAuth2 Integration

#### Supported Providers

- **Google**: OAuth2 Authorization Code flow
- **GitHub**: OAuth2 Authorization Code flow
- **Microsoft**: OAuth2 Authorization Code flow

#### Security Measures

- **State Parameter**: CSRF protection via random state
- **Code Exchange**: Server-to-server token exchange
- **Scope Limiting**: Request minimum necessary scopes
- **Token Storage**: Tokens refreshed and stored securely

### 3. Session Management

#### Session Timeout

- **Access Token Expiration**: 24 hours
- **Refresh Token Expiration**: 30 days
- **Idle Session Timeout**: 24 hours of inactivity
- **Concurrent Sessions**: Maximum 3 per user

#### Session Invalidation

- Manual logout revokes all tokens
- Suspended accounts invalidate all sessions
- Password change invalidates refresh tokens
- Expired tokens automatically cleared from database

### 4. Role-Based Access Control (RBAC)

```python
# User Roles
- student: Can ask questions, view progress
- educator: Can manage students, view analytics
- admin: Full system access

# Permission Matrix
student → Read own data, create sessions, ask questions
educator → Read student data (assigned), manage content
admin → Full system access, user management, billing
```

---

## Data Protection

### 1. Encryption in Transit

- **Protocol**: HTTPS/TLS 1.3 minimum
- **Certificate**: AWS Certificate Manager managed
- **HSTS**: HTTP Strict Transport Security enabled
  ```
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  ```
- **Cipher Suites**: Only strong ciphers allowed
- **Certificate Pinning**: Public key pinning for API endpoints (future)

### 2. Encryption at Rest

- **Database**: MySQL with native encryption or AWS RDS encryption
- **Sensitive Fields**:
  - Passwords: Bcrypt hashes
  - API Keys: Encrypted with AWS KMS
  - PII: Optionally encrypted at rest
- **Secrets Management**: AWS Secrets Manager with rotation

### 3. PII & Data Classification

#### Data Classification

```
PUBLIC
├─ Anonymous usage statistics
└─ Public documentation

INTERNAL
├─ User email addresses
├─ Basic profile information
└─ Session timestamps

CONFIDENTIAL
├─ Password hashes
├─ API keys and tokens
├─ Conversation content
└─ Learning analytics
```

#### Data Handling

- **Collection**: Minimum necessary data collected
- **Retention**: Deleted after 90 days (user accounts) or per GDPR request
- **Access**: Only authorized services access sensitive data
- **Logging**: Sensitive data excluded from logs

### 4. Data Backup & Recovery

- **Backup Frequency**: Daily automated snapshots
- **Retention Period**: 35 days
- **Redundancy**: Multi-AZ replication
- **Encryption**: Backups encrypted at rest
- **Testing**: Monthly recovery testing
- **Documentation**: Restore procedures documented

---

## API Security

### 1. Rate Limiting

**Global Limits**:
- 10,000 requests/minute per IP

**Per-User Limits**:
- 100 requests/minute (standard user)
- 50 requests/minute (tutor endpoints)
- 5 requests/minute (authentication endpoints)

**Sliding Window Algorithm**:
```
Current rate = requests in last 60 seconds
If rate >= limit, reject with 429 (Too Many Requests)
```

**Headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1719201600
Retry-After: 60
```

### 2. Input Validation

**Validation Strategy**:
- Whitelist acceptable input
- Reject by default
- Validate on both client and server

**Implementation**:
- Pydantic schemas enforce types
- Regex patterns for format validation
- Length limits on all strings
- Numeric bounds checking

**Example**:
```python
class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000)
    topic: str = Field(..., max_length=100)
    context: Optional[str] = Field(None, max_length=1000)
```

### 3. SQL Injection Prevention

- **ORM Usage**: SQLAlchemy prevents SQL injection
- **Parameterized Queries**: All queries parameterized
- **No Dynamic Queries**: Never concatenate user input
- **Stored Procedures**: Not used (prefer ORM)

```python
# ✓ Safe (SQLAlchemy)
user = db.query(User).filter(User.email == user_email).first()

# ✗ Dangerous (Never do this)
query = f"SELECT * FROM user WHERE email = '{user_email}'"
```

### 4. Cross-Site Scripting (XSS) Prevention

**Content Security Policy**:
```
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'
```

**Response Sanitization**:
- Escape HTML special characters
- Remove script tags
- Validate JSON responses

**Frontend Protection**:
- Use innerHTML carefully, prefer textContent
- Sanitize API responses
- Avoid eval() and similar functions

### 5. Cross-Site Request Forgery (CSRF) Protection

**CSRF Tokens**:
- State parameter in OAuth2 flow
- Optional CSRF tokens for state-changing operations
- Token stored in HTTP-only cookies
- Token validated on every state-changing request

### 6. CORS Configuration

**Allowed Origins**:
```
development: http://localhost:3000, http://localhost:8080
staging: https://staging.thinkloop.ai
production: https://thinkloop.ai
```

**Allowed Methods**:
- GET, POST, PUT, DELETE, OPTIONS

**Allowed Headers**:
- Content-Type, Authorization, X-Requested-With

**Credentials**: Included only for trusted origins

---

## Vulnerability Disclosure

### Reporting a Vulnerability

**DO NOT** create public GitHub issues for security vulnerabilities.

Instead, email: **security@thinkloop.ai**

Include:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Initial Response**: Within 24 hours
- **Investigation**: Within 5 business days
- **Fix Development**: Depends on severity
- **Public Disclosure**: After fix is deployed and tested

### Severity Levels

| Severity | CVSS Score | Response Time | Example |
|----------|-----------|---------------|---------|
| Critical | 9.0-10.0 | Immediate | Remote code execution |
| High | 7.0-8.9 | 24 hours | Authentication bypass |
| Medium | 4.0-6.9 | 7 days | Data exposure |
| Low | 0.1-3.9 | 30 days | Minor information disclosure |

### Bug Bounty Program

We have a responsible disclosure program. Eligible researchers may qualify for:
- Public recognition
- $100-$5,000+ bounty (depending on severity)
- Professional opportunities

Contact: security@thinkloop.ai for details.

---

## Security Best Practices

### For Developers

1. **Use Latest Dependencies**
   ```bash
   # Check for vulnerable packages
   pip check
   # Update to latest versions
   pip install --upgrade -r requirements.txt
   ```

2. **Secrets Management**
   - Never commit secrets to Git
   - Use environment variables or AWS Secrets Manager
   - Rotate secrets regularly

3. **Code Review**
   - Security-focused code review required
   - Use automated security scanning (bandit)
   - Check for OWASP vulnerabilities

4. **Logging**
   - Never log sensitive data (passwords, tokens)
   - Include user ID in logs for tracing
   - Log authentication failures

5. **Testing**
   - Include security tests
   - Test authentication edge cases
   - Test authorization boundaries

### For Operations

1. **Monitoring**
   - CloudWatch Logs enabled
   - AlertsConfigured for suspicious activity
   - Real-time threat detection

2. **Patching**
   - Monthly dependency updates
   - Security patches applied immediately
   - Regular testing of patches

3. **Access Control**
   - IAM roles with least privilege
   - API keys rotated regularly
   - 2FA for admin access (future)

4. **Backup & Disaster Recovery**
   - Daily backups tested
   - Restore procedures documented
   - RTO < 4 hours, RPO < 1 hour

---

## Compliance

### Standards & Frameworks

#### GDPR (General Data Protection Regulation)
- ✓ Data processing agreements
- ✓ User consent collection
- ✓ Data export capabilities
- ✓ Data deletion on request
- ✓ Privacy policy published

#### COPPA (Children's Online Privacy Protection Act)
- ✓ Age verification for underage users
- ✓ Parental consent requirements
- ✓ Limited data collection for minors
- ✓ No behavioral targeting of minors

#### SOC 2 Type II (Target)
- ✓ Security controls documented
- ✓ Change management procedures
- ✓ Audit logging enabled
- ✓ Annual audit planned

#### OWASP Top 10 Protection

| Vulnerability | Protection |
|---------------|-----------|
| Injection | Parameterized queries, input validation |
| Broken Auth | JWT, OAuth2, session management |
| Sensitive Data Exposure | Encryption in transit and at rest |
| XML External Entities (XXE) | XML parsing disabled |
| Broken Access Control | RBAC, authorization checks |
| Security Misconfiguration | Security hardening guides |
| XSS | Input/output encoding, CSP |
| Insecure Deserialization | No unsafe deserialization |
| Using Components with Known Vulns | Dependency scanning |
| Insufficient Logging | Comprehensive logging |

---

## Incident Response

### Incident Classification

| Level | Type | Examples | Response Time |
|-------|------|----------|----------------|
| Critical | System down, data breach | Ransomware, DDoS | Immediate |
| High | Service degradation | Authentication failure | 1 hour |
| Medium | Unexpected behavior | Bugs affecting functionality | 4 hours |
| Low | Minor issues | UI glitches | 24 hours |

### Incident Response Plan

1. **Detection**: Automated monitoring alerts
2. **Response**: Immediate incident commander assignment
3. **Investigation**: Root cause analysis
4. **Remediation**: Fix deployed and tested
5. **Communication**: Status updates to users
6. **Post-Mortem**: Analysis and improvements

### Contact Information

- **Security**: security@thinkloop.ai
- **Incident Response**: incidents@thinkloop.ai
- **General Support**: support@thinkloop.ai

---

## Security Checklist

- [ ] All dependencies up-to-date
- [ ] No secrets in code
- [ ] Input validation on all endpoints
- [ ] Authentication required for sensitive operations
- [ ] HTTPS/TLS enabled
- [ ] Rate limiting configured
- [ ] Logging enabled and monitored
- [ ] Backups tested
- [ ] Security tests passing
- [ ] Code review completed
- [ ] Security scan passed (bandit, snyk)
- [ ] Documentation updated

---

**Document Owner**: Security Team  
**Last Updated**: July 2026  
**Next Review**: August 2026

For questions or concerns, contact: security@thinkloop.ai
