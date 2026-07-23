# API Specification Document
# thinkloop AI

**Version**: 1.0  
**Last Updated**: July 2026  
**Base URL**: `https://api.thinkloop.ai/api/v1`  
**Status**: Active

---

## 1. API Overview

### Base Information

- **Protocol**: REST over HTTPS
- **Version**: 1.0
- **Format**: JSON
- **Authentication**: JWT Bearer Token
- **Rate Limit**: 100 requests/minute per user
- **Response Timeout**: 30 seconds

### API Documentation

- **Swagger/OpenAPI**: `/docs`
- **ReDoc**: `/redoc`
- **OpenAPI JSON**: `/openapi.json`

---

## 2. Authentication Endpoints

### 2.1 User Registration

**Endpoint**: `POST /auth/register`

**Description**: Create a new user account

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "username": "john_doe",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Request Schema**:
- `email`: String, email format, max 255 chars, required
- `password`: String, min 8 chars, must contain uppercase, lowercase, digit, special char
- `username`: String, alphanumeric + underscore, 3-30 chars, unique
- `first_name`: String, max 100 chars, optional
- `last_name`: String, max 100 chars, optional

**Response** (201 Created):
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "john_doe",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2026-07-23T10:30:45Z",
  "message": "Registration successful. Check your email to verify your account."
}
```

**Status Codes**:
- `201 Created`: Registration successful
- `400 Bad Request`: Invalid input
- `409 Conflict`: Email or username already exists

**Errors**:
```json
{
  "error": "DUPLICATE_EMAIL",
  "message": "Email already registered",
  "details": {
    "field": "email",
    "constraint": "unique"
  }
}
```

---

### 2.2 User Login

**Endpoint**: `POST /auth/login`

**Description**: Authenticate user and obtain JWT token

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "user": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "john_doe",
    "role": "student",
    "is_verified": true
  }
}
```

**Status Codes**:
- `200 OK`: Login successful
- `400 Bad Request`: Invalid credentials
- `401 Unauthorized`: Email not verified
- `404 Not Found`: User not found

**Headers**:
- `Set-Cookie`: HttpOnly refresh token cookie

---

### 2.3 Refresh Token

**Endpoint**: `POST /auth/refresh`

**Description**: Get new access token using refresh token

**Request Headers**:
```
Authorization: Bearer {refresh_token}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

**Status Codes**:
- `200 OK`: Token refreshed
- `401 Unauthorized`: Invalid or expired refresh token

---

### 2.4 Logout

**Endpoint**: `POST /auth/logout`

**Description**: Invalidate current session and refresh token

**Request Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "message": "Logout successful"
}
```

**Status Codes**:
- `200 OK`: Logout successful
- `401 Unauthorized`: Not authenticated

---

### 2.5 OAuth2 Login

**Endpoint**: `GET /auth/oauth/authorize`

**Description**: Initiate OAuth2 flow

**Query Parameters**:
- `provider`: String (google, github, microsoft), required
- `state`: String, random state for CSRF protection, required
- `redirect_uri`: String, must be whitelisted, required

**Redirect**: User to provider's authorization endpoint

---

### 2.6 OAuth2 Callback

**Endpoint**: `POST /auth/oauth/callback`

**Description**: Handle OAuth2 provider callback

**Request**:
```json
{
  "provider": "google",
  "code": "4/0AY7...",
  "state": "random_state_string"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@google.com",
    "username": "john_doe",
    "is_verified": true
  }
}
```

---

## 3. Tutor Endpoints

### 3.1 Ask Question

**Endpoint**: `POST /tutor/ask`

**Description**: Ask the AI tutor a question

**Request Headers**:
```
Authorization: Bearer {access_token}
```

**Request**:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "question": "How do I implement a binary search algorithm?",
  "topic": "Data Structures",
  "context": "I'm studying for interviews"
}
```

**Request Schema**:
- `session_id`: UUID, optional (creates new if not provided)
- `question`: String, 1-5000 chars, required
- `topic`: String, max 100 chars, optional
- `context`: String, max 1000 chars, optional

**Response** (200 OK):
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "session_id": "550e8400-e29b-41d4-a716-446655440001",
  "question": "How do I implement a binary search algorithm?",
  "response": "Great question! Let me ask you a clarifying question first: What's your current understanding of how binary search differs from linear search?",
  "response_time_ms": 245,
  "hint_level": 0,
  "can_request_hint": true,
  "can_reveal_answer": false,
  "misconception_detected": false,
  "created_at": "2026-07-23T10:30:45Z"
}
```

**Status Codes**:
- `200 OK`: Response generated successfully
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Not authenticated
- `429 Too Many Requests`: Rate limit exceeded

---

### 3.2 Request Hint

**Endpoint**: `POST /tutor/hint`

**Description**: Request a hint for current question

**Request Headers**:
```
Authorization: Bearer {access_token}
```

**Request**:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response** (200 OK):
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "hint_level": 1,
  "hint": "Consider: what property of the sorted array allows us to eliminate half of the remaining elements in each step?",
  "next_hint_available_at": "2026-07-23T10:35:45Z",
  "hints_remaining": 5,
  "can_reveal_answer": false
}
```

**Hint Levels**:
- `1`: Conceptual question
- `2`: Conceptual hint explaining key concept
- `3`: Directional hint pointing toward solution
- `4`: Code structure hint
- `5`: Nearly complete with minor gaps
- `6`: Complete answer with explanation

**Status Codes**:
- `200 OK`: Hint provided
- `400 Bad Request`: Invalid conversation ID
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: No hints remaining for this question
- `429 Too Many Requests`: Rate limit exceeded

---

### 3.3 Check Answer

**Endpoint**: `POST /tutor/check`

**Description**: Submit an answer for evaluation

**Request**:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "answer": "function binarySearch(arr, target) { ... }",
  "answer_type": "code"
}
```

**Response** (200 OK):
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "is_correct": false,
  "feedback": "Good attempt! Your logic is almost right, but there's an issue with your loop condition. What happens when mid equals target?",
  "misconception_detected": true,
  "misconception_details": {
    "type": "off_by_one_error",
    "description": "Loop doesn't handle equal case properly"
  },
  "score": 70,
  "suggestions": "Try tracing through your code with a small array to verify the behavior"
}
```

**Status Codes**:
- `200 OK`: Answer evaluated
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Not authenticated

---

### 3.4 Reveal Answer

**Endpoint**: `POST /tutor/reveal`

**Description**: Request complete answer (unlocked after sufficient hints)

**Request**:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response** (200 OK):
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "complete_answer": "function binarySearch(arr, target) {\n  let left = 0;\n  let right = arr.length - 1;\n  while (left <= right) {\n    const mid = Math.floor((left + right) / 2);\n    if (arr[mid] === target) return mid;\n    if (arr[mid] < target) left = mid + 1;\n    else right = mid - 1;\n  }\n  return -1;\n}",
  "explanation": "This solution uses two pointers to track the search range. In each iteration, we eliminate half of the remaining elements, achieving O(log n) time complexity...",
  "key_concepts": ["divide and conquer", "time complexity", "pointer manipulation"],
  "practice_problems": [
    {"title": "Search in Rotated Sorted Array", "difficulty": "medium"},
    {"title": "Find First and Last Position", "difficulty": "medium"}
  ]
}
```

**Status Codes**:
- `200 OK`: Answer revealed
- `400 Bad Request`: Answer not yet available
- `401 Unauthorized`: Not authenticated

---

### 3.5 Get Debugging Help

**Endpoint**: `POST /tutor/debug`

**Description**: Get help debugging code

**Request**:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "code": "function binarySearch(arr, target) { ... }",
  "error": "Returns wrong result for [1,3,5,7], target=3",
  "language": "javascript"
}
```

**Response** (200 OK):
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "debugging_steps": [
    "What is the first value of mid in your example?",
    "What happens when arr[mid] equals the target?"
  ],
  "suggested_tools": ["console.log for tracing", "debugger breakpoints"],
  "common_mistakes": ["Off-by-one errors in array indexing"]
}
```

---

## 4. Session Management Endpoints

### 4.1 Create Session

**Endpoint**: `POST /sessions`

**Description**: Create new learning session

**Request**:
```json
{
  "topic": "Data Structures",
  "title": "Binary Search Interview Prep",
  "description": "Preparing for technical interviews"
}
```

**Response** (201 Created):
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "550e8400-e29b-41d4-a716-446655440001",
  "topic": "Data Structures",
  "title": "Binary Search Interview Prep",
  "status": "active",
  "created_at": "2026-07-23T10:30:45Z"
}
```

---

### 4.2 List Sessions

**Endpoint**: `GET /sessions`

**Description**: Get user's sessions

**Query Parameters**:
- `limit`: Integer, max 100, default 20
- `offset`: Integer, default 0
- `status`: String (active, completed, paused)
- `topic`: String, filter by topic

**Response** (200 OK):
```json
{
  "sessions": [
    {
      "session_id": "550e8400-e29b-41d4-a716-446655440000",
      "topic": "Data Structures",
      "title": "Binary Search Interview Prep",
      "status": "active",
      "question_count": 5,
      "created_at": "2026-07-23T10:30:45Z"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

---

### 4.3 Get Session Details

**Endpoint**: `GET /sessions/{session_id}`

**Description**: Get detailed session information

**Response** (200 OK):
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "topic": "Data Structures",
  "title": "Binary Search Interview Prep",
  "status": "active",
  "total_questions": 5,
  "total_hints_used": 2,
  "average_response_time_ms": 312,
  "misconceptions_found": 1,
  "created_at": "2026-07-23T10:30:45Z",
  "updated_at": "2026-07-23T11:30:45Z"
}
```

---

### 4.4 Get Session Conversation History

**Endpoint**: `GET /sessions/{session_id}/history`

**Description**: Get all interactions in a session

**Query Parameters**:
- `limit`: Integer, max 100, default 50
- `offset`: Integer, default 0

**Response** (200 OK):
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "interactions": [
    {
      "conversation_id": "550e8400-e29b-41d4-a716-446655440010",
      "question": "How do I implement binary search?",
      "response": "Let me ask you a clarifying question...",
      "hint_level": 2,
      "misconception_detected": false,
      "created_at": "2026-07-23T10:30:45Z"
    }
  ],
  "total": 5,
  "limit": 50,
  "offset": 0
}
```

---

### 4.5 Close Session

**Endpoint**: `POST /sessions/{session_id}/close`

**Description**: End a learning session

**Request**:
```json
{
  "feedback": "Great session, learned a lot!",
  "rating": 5
}
```

**Response** (200 OK):
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "closed_at": "2026-07-23T12:30:45Z"
}
```

---

## 5. Analytics Endpoints

### 5.1 Get User Progress

**Endpoint**: `GET /analytics/progress`

**Description**: Get user's learning progress

**Query Parameters**:
- `topic`: String, optional filter by topic
- `period`: String (week, month, all), default all

**Response** (200 OK):
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_sessions": 12,
  "total_questions": 47,
  "total_hints_used": 15,
  "average_session_duration_min": 23.5,
  "topics": [
    {
      "name": "Data Structures",
      "progress": 75,
      "questions_asked": 20,
      "status": "in_progress"
    },
    {
      "name": "Algorithms",
      "progress": 100,
      "questions_asked": 15,
      "status": "mastered"
    }
  ],
  "weekly_activity": [
    {"date": "2026-07-21", "sessions": 3, "questions": 8},
    {"date": "2026-07-22", "sessions": 2, "questions": 6}
  ]
}
```

---

### 5.2 Get Learning Insights

**Endpoint**: `GET /analytics/insights`

**Description**: Get personalized learning insights

**Response** (200 OK):
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "strengths": [
    "Time Complexity Analysis",
    "Recursion fundamentals"
  ],
  "areas_to_improve": [
    "Dynamic Programming",
    "Graph Algorithms"
  ],
  "misconceptions": [
    {
      "topic": "Binary Search",
      "misconception": "Off-by-one errors in loop conditions",
      "resolved": false
    }
  ],
  "recommended_topics": [
    "Advanced Dynamic Programming",
    "Graph Traversal Algorithms"
  ],
  "learning_velocity": "accelerating",
  "next_milestone": "Complete 50 total questions"
}
```

---

### 5.3 Export Learning Transcript

**Endpoint**: `GET /analytics/transcript`

**Description**: Export learning data as PDF

**Query Parameters**:
- `format`: String (pdf, csv), default pdf

**Response**: PDF file download (application/pdf)

---

## 6. Admin Endpoints

### 6.1 List Users (Admin)

**Endpoint**: `GET /admin/users`

**Description**: List all users (admin only)

**Query Parameters**:
- `limit`: Integer, max 100, default 20
- `offset`: Integer, default 0
- `role`: String (student, educator, admin)
- `status`: String (active, suspended)

**Response** (200 OK):
```json
{
  "users": [
    {
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "username": "john_doe",
      "role": "student",
      "is_active": true,
      "created_at": "2026-07-23T10:30:45Z",
      "last_login": "2026-07-23T11:00:00Z"
    }
  ],
  "total": 150,
  "limit": 20,
  "offset": 0
}
```

---

### 6.2 Suspend User (Admin)

**Endpoint**: `POST /admin/users/{user_id}/suspend`

**Description**: Suspend a user account

**Request**:
```json
{
  "reason": "Terms of service violation"
}
```

**Response** (200 OK):
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "is_active": false,
  "suspended_at": "2026-07-23T12:30:45Z"
}
```

---

### 6.3 System Health

**Endpoint**: `GET /health`

**Description**: System health check

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2026-07-23T10:30:45Z",
  "components": {
    "database": "connected",
    "cache": "connected",
    "openai_api": "available"
  },
  "uptime_seconds": 123456,
  "version": "1.0.0"
}
```

---

## 7. Error Handling

### Standard Error Response Format

```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": {
    "field": "email",
    "constraint": "unique"
  },
  "request_id": "req-123-456",
  "timestamp": "2026-07-23T10:30:45Z"
}
```

### Common HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Duplicate resource |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | Internal server error |
| 503 | Service Unavailable | Temporary maintenance |

---

## 8. Rate Limiting

**Rate Limit Headers** (included in every response):
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1719201600
```

**Limits by Endpoint**:
- `/tutor/ask`: 50 requests/minute
- `/tutor/hint`: 30 requests/minute
- `/auth/*`: 5 requests/minute (brute force protection)
- `/admin/*`: 100 requests/minute

---

## 9. Pagination

**Pagination Parameters**:
- `limit`: Items per page (1-100, default 20)
- `offset`: Number of items to skip (default 0)

**Pagination Response**:
```json
{
  "data": [...],
  "total": 150,
  "limit": 20,
  "offset": 0,
  "has_more": true
}
```

---

## 10. Versioning

**URL Versioning**: `/api/v1/...`

**Deprecation Policy**:
- Minimum 12 months notice before breaking changes
- Deprecation header included in responses
- `/api/v2` for major changes

---

**Document Owner**: API Design Team  
**Last Updated**: July 2026
