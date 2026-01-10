# SQLite version for easy development and testing
# Use this instead of database.py if you don't have SQL Server setup

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # SQLite database - creates a local file
    database_url: str = "sqlite:///./skill_swap.db"
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()

# Create SQLite engine
engine = create_engine(
    settings.database_url, 
    connect_args={"check_same_thread": False}  # Required for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables immediately for SQLite
def create_sqlite_tables():
    """Create all tables for SQLite database"""
    Base.metadata.create_all(bind=engine)
    print("SQLite database and tables created successfully!")

# Auto-create tables when this module is imported
create_sqlite_tables()
