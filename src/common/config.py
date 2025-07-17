import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Telegram API credentials
    telegram_api_id: str = os.getenv("TELEGRAM_API_ID")
    telegram_api_hash: str = os.getenv("TELEGRAM_API_HASH")
    telegram_phone: str = os.getenv("TELEGRAM_PHONE")
    
    # Database configuration
    postgres_user: str = os.getenv("POSTGRES_USER")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD")
    postgres_db: str = os.getenv("POSTGRES_DB")
    postgres_host: str = os.getenv("POSTGRES_HOST")
    postgres_port: str = os.getenv("POSTGRES_PORT")
    
    # Application settings
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    data_dir: str = os.getenv("DATA_DIR", "./data")
    
    class Config:
        env_file = ".env"

settings = Settings()