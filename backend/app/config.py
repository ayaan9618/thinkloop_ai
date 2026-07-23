"""
Application Configuration
Handles environment variables and app settings
"""

from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")

    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    workers: int = Field(default=1, env="WORKERS")

    # Database
    database_url: str = Field(
        default="mysql+pymysql://root:password@localhost:3306/thinkloop_ai",
        env="DATABASE_URL",
    )
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")
    database_pool_size: int = Field(default=20, env="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(default=40, env="DATABASE_MAX_OVERFLOW")

    # JWT
    jwt_secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        env="JWT_SECRET_KEY",
    )
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(
        default=1440,  # 24 hours
        env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    jwt_refresh_token_expire_days: int = Field(
        default=30,
        env="JWT_REFRESH_TOKEN_EXPIRE_DAYS",
    )

    # OAuth2
    google_client_id: Optional[str] = Field(default=None, env="GOOGLE_CLIENT_ID")
    google_client_secret: Optional[str] = Field(
        default=None, env="GOOGLE_CLIENT_SECRET"
    )
    github_client_id: Optional[str] = Field(default=None, env="GITHUB_CLIENT_ID")
    github_client_secret: Optional[str] = Field(
        default=None, env="GITHUB_CLIENT_SECRET"
    )
    microsoft_client_id: Optional[str] = Field(default=None, env="MICROSOFT_CLIENT_ID")
    microsoft_client_secret: Optional[str] = Field(
        default=None, env="MICROSOFT_CLIENT_SECRET"
    )

    # OpenAI
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    openai_temperature: float = Field(default=0.7, env="OPENAI_TEMPERATURE")
    openai_timeout: int = Field(default=30, env="OPENAI_TIMEOUT")

    # AWS
    aws_region: str = Field(default="us-east-1", env="AWS_REGION")
    aws_access_key_id: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(
        default=None, env="AWS_SECRET_ACCESS_KEY"
    )
    aws_secrets_manager_name: Optional[str] = Field(
        default=None, env="AWS_SECRETS_MANAGER_NAME"
    )

    # CORS
    cors_origins: list = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:8000",
            "http://localhost",
        ],
        env="CORS_ORIGINS",
    )
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    cors_allow_methods: list = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        env="CORS_ALLOW_METHODS",
    )
    cors_allow_headers: list = Field(
        default=["Content-Type", "Authorization"],
        env="CORS_ALLOW_HEADERS",
    )

    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    rate_limit_requests_per_minute: int = Field(
        default=100, env="RATE_LIMIT_REQUESTS_PER_MINUTE"
    )
    rate_limit_tutor_requests_per_minute: int = Field(
        default=50, env="RATE_LIMIT_TUTOR_REQUESTS_PER_MINUTE"
    )
    rate_limit_auth_requests_per_minute: int = Field(
        default=5, env="RATE_LIMIT_AUTH_REQUESTS_PER_MINUTE"
    )

    # Session
    session_timeout_minutes: int = Field(
        default=1440,  # 24 hours
        env="SESSION_TIMEOUT_MINUTES",
    )
    session_max_concurrent: int = Field(
        default=3, env="SESSION_MAX_CONCURRENT"
    )

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")

    # Feature Flags
    feature_oauth2_enabled: bool = Field(default=True, env="FEATURE_OAUTH2_ENABLED")
    feature_hints_enabled: bool = Field(default=True, env="FEATURE_HINTS_ENABLED")
    feature_analytics_enabled: bool = Field(
        default=True, env="FEATURE_ANALYTICS_ENABLED"
    )
    feature_misconception_detection: bool = Field(
        default=True, env="FEATURE_MISCONCEPTION_DETECTION"
    )

    # Testing
    testing_mode: bool = Field(default=False, env="TESTING_MODE")
    mock_openai: bool = Field(default=False, env="MOCK_OPENAI")

    # Security
    secure_cookies: bool = Field(default=True, env="SECURE_COOKIES")
    hsts_enabled: bool = Field(default=True, env="HSTS_ENABLED")
    csp_enabled: bool = Field(default=True, env="CSP_ENABLED")

    class Config:
        """Pydantic settings configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Export settings
settings = get_settings()
