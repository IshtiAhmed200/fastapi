from pydantic_settings import BaseSettings

class Configuration(BaseSettings):


    @property
    def DATABASE_URL(self):
        return "sqlite:///./app.db"

