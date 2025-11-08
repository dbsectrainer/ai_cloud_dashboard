"""Application settings using Pydantic for type-safe configuration."""

from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "AI Cloud Dashboard"
    APP_VERSION: str = "0.2.0"
    DEBUG: bool = False
    ENVIRONMENT: str = Field(default="development", pattern="^(development|staging|production)$")

    # Data paths
    DATA_DIR: Path = Field(default=Path("data/warehouse"))
    CACHE_DIR: Path = Field(default=Path("data/cache"))
    EXPORT_DIR: Path = Field(default=Path("data/exports"))

    # Database
    DATABASE_URL: Optional[str] = Field(
        default=None,
        description="PostgreSQL connection string",
    )

    # Object Storage (MinIO/S3)
    MINIO_ENDPOINT: Optional[str] = None
    MINIO_ACCESS_KEY: Optional[str] = None
    MINIO_SECRET_KEY: Optional[str] = None
    MINIO_SECURE: bool = False
    MINIO_BUCKET: str = "cloud-dashboard"

    # Observability
    OTEL_ENDPOINT: Optional[str] = Field(
        default=None,
        description="OpenTelemetry collector endpoint (HTTP)",
    )
    OTEL_SERVICE_NAME: str = "cloud-dashboard"
    PROMETHEUS_URL: Optional[str] = None
    ENABLE_TELEMETRY: bool = True

    # Features
    ENABLE_AI_INSIGHTS: bool = True
    ENABLE_DATA_EXPORT: bool = True
    ENABLE_REAL_TIME_UPDATES: bool = False

    # Data ingestion
    INGESTION_ENABLED: bool = True
    INGESTION_INTERVAL_HOURS: int = Field(default=24, ge=1, le=168)
    AWS_PRICING_URL: str = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json"
    AZURE_PRICING_URL: str = "https://prices.azure.com/api/retail/prices"
    GCP_PRICING_URL: str = "https://cloudbilling.googleapis.com/v1/services/6F81-5844-456A/skus"

    # Cache settings
    CACHE_TTL_SECONDS: int = Field(default=3600, ge=60)
    CACHE_MAX_SIZE_MB: int = Field(default=500, ge=10)

    # API rate limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(default=60, ge=1)

    # Security
    ALLOWED_ORIGINS: list[str] = Field(default_factory=lambda: ["http://localhost:8501"])
    SECRET_KEY: str = Field(
        default="change-me-in-production",
        min_length=32,
    )

    @field_validator("DATA_DIR", "CACHE_DIR", "EXPORT_DIR")
    @classmethod
    def ensure_path_exists(cls, v: Path) -> Path:
        """Ensure directories exist."""
        v.mkdir(parents=True, exist_ok=True)
        return v

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str, info) -> str:
        """Warn if using default secret key in production."""
        if info.data.get("ENVIRONMENT") == "production" and v == "change-me-in-production":
            raise ValueError("SECRET_KEY must be changed in production environment")
        return v

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.ENVIRONMENT == "development"


# Global settings instance
settings = Settings()
