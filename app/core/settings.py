from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    GOOGLE_TOKEN_ID: str = "ajqas9d7fa90s7df22bLUylnkLlnhjhAS7"
    DATABASE_URL: str = ""

    REDIS_HOST: str = "cache"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None


settings = Settings()
