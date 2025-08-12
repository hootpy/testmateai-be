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

    class Config:
        case_sensitive = True
        env_file = ".env"


SETTINGS = Settings()
