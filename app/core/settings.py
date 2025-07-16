from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "hgHDASVJJHdkgj234vkjVQ4V3JV3vbasd90d12A"
    ALGORYTHM:str = "HS256"
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()
