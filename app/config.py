from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os


class Settings(BaseSettings):
    # Telegram Bot
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    
    # Database
    database_url: str = Field(default="sqlite+aiosqlite:///./test_bot.db", env="DATABASE_URL")
    
    # API
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_secret_key: str = Field(..., env="API_SECRET_KEY")
    
    # Yandex Maps
    yandex_maps_api_key: str = Field(default="", env="YANDEX_MAPS_API_KEY")
    
    # File Storage
    uploads_dir: str = Field(default="./app/static/uploads", env="UPLOADS_DIR")
    photos_dir: str = Field(default="./app/static/photos", env="PHOTOS_DIR")
    max_file_size: int = Field(default=10485760, env="MAX_FILE_SIZE")  # 10MB
    
    # Admin
    admin_phones: str = Field(default="", env="ADMIN_PHONES")
    
    @property
    def admin_phone_list(self) -> List[str]:
        if not self.admin_phones:
            return []
        return [phone.strip() for phone in self.admin_phones.split(",") if phone.strip()]
    
    # Rasa
    rasa_server_url: str = Field(default="http://localhost:5005", env="RASA_SERVER_URL")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Ensure directories exist
os.makedirs(settings.uploads_dir, exist_ok=True)
os.makedirs(settings.photos_dir, exist_ok=True)
