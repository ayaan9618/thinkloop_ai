# GitHub Actions Secrets Configuration

This document explains how to configure GitHub Secrets for CI/CD pipelines.

## 📋 Required Secrets

### AWS Configuration

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION                 # e.g., us-east-1
EB_BUCKET                  # S3 bucket for Elastic Beanstalk deployments
```

### Database Configuration

For local testing in CI, database configuration is handled in the workflow file. For production:

```
PROD_DATABASE_URL          # MySQL connection string for production
STAGING_DATABASE_URL       # MySQL connection string for staging
```

### OpenAI Configuration

```
OPENAI_API_KEY            # API key for OpenAI GPT-4/3.5
```

### Slack Notifications

```
SLACK_WEBHOOK             # Webhook URL for Slack notifications
```

### GitHub Token

```
GITHUB_TOKEN              # Automatically provided by GitHub Actions
```

## 🔐 How to Add Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Enter the secret name (e.g., `AWS_ACCESS_KEY_ID`)
5. Enter the secret value
6. Click **Add secret**

## 📝 Secret Values

### AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY

Create AWS IAM user with Elastic Beanstalk permissions:

```bash
# AWS CLI command to create user
aws iam create-user --user-name github-actions

# Attach policy
aws iam attach-user-policy --user-name github-actions \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Create access key
aws iam create-access-key --user-name github-actions
```

### AWS_REGION

```
us-east-1    # US East (Virginia)
eu-west-1   # EU (Ireland)
ap-southeast-1  # Asia Pacific (Singapore)
```

### EB_BUCKET

Create S3 bucket for Elastic Beanstalk:

```bash
aws s3 mb s3://thinkloop-ai-deployments-YOUR-ACCOUNT-ID
```

### OPENAI_API_KEY

Get from [OpenAI API Keys](https://platform.openai.com/api-keys)

### SLACK_WEBHOOK

Create incoming webhook in Slack:

1. Go to your Slack workspace
2. Create a new app or select existing
3. Enable **Incoming Webhooks**
4. Click **Add New Webhook to Workspace**
5. Select channel
6. Copy webhook URL

## ✅ Testing Secrets in Local Environment

Create `.env` file locally with the same secrets:

```bash
# .env (never commit this!)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
OPENAI_API_KEY=your_openai_key
SLACK_WEBHOOK=your_slack_webhook
```

Then run locally:

```bash
docker-compose up -d
pytest backend/tests/
```

## 🔄 Rotating Secrets

### To rotate AWS credentials:

```bash
# Create new access key
aws iam create-access-key --user-name github-actions

# Update GitHub secret with new key

# Delete old access key
aws iam delete-access-key --user-name github-actions --access-key-id OLD_KEY_ID
```

### To rotate other secrets:

1. Generate new secret value
2. Update in GitHub Secrets
3. Verify workflows still work
4. Deactivate old secret in the service (e.g., OpenAI, Slack)

## 🚀 CI/CD Workflows Using Secrets

### CI Pipeline (.github/workflows/ci.yml)

- Runs on every push and PR
- No secrets needed (uses public tools)

### Deploy Pipeline (.github/workflows/deploy.yml)

- Runs on push to main or manual trigger
- Uses: `AWS_*`, `EB_BUCKET`, `SLACK_WEBHOOK`
- Builds Docker image and pushes to ECR
- Deploys to Elastic Beanstalk

## 📊 Secret Usage Audit

Check where secrets are used:

```bash
# Search workflows
grep -r "secrets\." .github/workflows/

# Search environment
grep -r "GITHUB_TOKEN\|AWS_\|OPENAI_" .github/workflows/
```

## 🛡️ Security Best Practices

1. ✅ Use separate credentials for staging and production
2. ✅ Rotate secrets every 90 days
3. ✅ Use least-privilege IAM policies
4. ✅ Never commit secrets to git
5. ✅ Enable audit logging for secret access
6. ✅ Use environment protection rules
7. ✅ Limit who can approve deployments

## 🚨 Troubleshooting

### Workflow fails with "authentication failed"

- Verify secret value is correct
- Check secret is in the repository (not organization)
- Verify branch protection rules

### Secret appears in logs

- Search workflow logs for accidental exposure
- Rotate the secret immediately
- Remove logs from GitHub Actions history

### Secrets not available to workflow

- Verify secret name matches exactly (case-sensitive)
- Check branch is allowed to use secret
- Verify repository has access to secrets

---

For more info, see [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
