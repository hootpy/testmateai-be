from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOG_ENV: str = "CONSOLE"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = True

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DATABASE: str
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str

    ALLOW_ORIGINS: list[str]
    ALLOW_CREDENTIALS: bool
    ALLOW_METHODS: list[str]
    ALLOW_HEADERS: list[str]

    # SMTP / Email settings (defaults configured for Gmail)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_USE_TLS: bool = True
    SMTP_FROM_EMAIL: str | None = None
    SMTP_FROM_NAME: str = "No-Reply"

    # OTP/Auth settings
    OTP_LENGTH: int = 6
    OTP_TTL_SECONDS: int = 120
    OTP_RATE_LIMIT_SECONDS: int = 30

    JWT_SECRET: str = "changeme"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7

    # LLM / AI configuration
    # Default provider is a local fake provider that echoes the prompt
    LLM_PROVIDER: str = "fake"
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    class Config:
        case_sensitive = True
        env_file = ".env"


SETTINGS = Settings()
