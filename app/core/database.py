import sqlite3
from app.core.settings import Settings

settings  = Settings()

def get_db_connection()->sqlite3.Connection:
    return sqlite3.connect(settings.DB_NAME)