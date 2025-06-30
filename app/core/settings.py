from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    GOOGLE_TOKEN_ID: str = "ajqas9d7fa90s7df22bLUylnkLlnhjhAS7"
    DB_NAME:str = 'pomodoro.db'
    DB_TYPE:str = 'sqlite'

settings = Settings()