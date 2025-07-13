from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
