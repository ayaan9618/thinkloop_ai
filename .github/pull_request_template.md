<!-- Pull Request Template -->
<!-- Please fill out all sections below. PRs that don't follow this template may be rejected. -->

## 🎯 Related Issue

Fixes #(issue number)
Related to #(issue number)

## 📝 Description

Provide a clear and concise description of the changes made in this PR.

### Changes Made
- Change 1
- Change 2
- Change 3

### Why These Changes?

Explain the reasoning behind these changes and any context that's helpful for reviewers.

## 🧪 Testing

### How was this tested?
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

### Test Coverage
```
Coverage: XX%
Previous: XX%
```

### Test Instructions

Step-by-step instructions to reproduce and verify the changes:
1. ...
2. ...
3. ...

## ✅ Checklist

- [ ] Code follows project style guidelines (PEP 8, Black formatting)
- [ ] Comments and docstrings are clear and complete
- [ ] No new warnings generated (linting passes)
- [ ] Type hints added to all functions
- [ ] Tests added for new functionality
- [ ] All tests pass locally (`pytest`)
- [ ] Code coverage is >= 80%
- [ ] No hardcoded secrets or sensitive data
- [ ] Database migrations included (if applicable)
- [ ] API documentation updated (if applicable)
- [ ] PR title follows conventional commits (feat:, fix:, docs:, etc.)

## 📚 Documentation

- [ ] README updated (if applicable)
- [ ] API_SPEC.md updated (if applicable)
- [ ] DATABASE_DESIGN.md updated (if applicable)
- [ ] Docstrings added/updated

## 🔐 Security

- [ ] No SQL injection vulnerabilities
- [ ] Input validation implemented
- [ ] Authentication/authorization checked
- [ ] No sensitive data in logs
- [ ] Security scan passes (bandit)

## 📊 Performance

- [ ] Performance impact assessed
- [ ] No N+1 queries introduced
- [ ] Caching considered where appropriate
- [ ] Load tested (if applicable)

## 🐛 Breaking Changes

- [ ] No breaking changes
- [ ] Breaking changes documented
- [ ] Migration path provided

## 📦 Dependencies

- [ ] No new dependencies added
- [ ] New dependencies are necessary and minimal
- [ ] Dependency versions are pinned

## 🚀 Deployment

- [ ] Ready for production
- [ ] Requires database migration
- [ ] Requires environment variable changes
- [ ] Requires configuration changes

**Environment Variables:**
```
None
```

**Configuration Changes:**
```
None
```

## 📸 Screenshots (if applicable)

Before:
<!-- Add before screenshot -->

After:
<!-- Add after screenshot -->

## 🔄 Reviewers

- @reviewer1
- @reviewer2

---

**Please review this PR carefully. We're committed to maintaining high code quality!**

Thank you for your contribution! 🙏
