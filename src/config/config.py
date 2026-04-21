from pydantic_settings import BaseSettings
from typing import Optional

class Configuration(BaseSettings):
    SECRET_KEY: Optional[str] = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def DATABASE_URL(self):
        return "sqlite:///./app.db"

config = Configuration()