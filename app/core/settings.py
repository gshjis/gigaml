from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    GOOGLE_TOKEN_ID: str = "ajqas9d7fa90s7df22bLUylnkLlnhjhAS7"
    DATABASE_URL: str = ""


settings = Settings()
