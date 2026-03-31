from pydantic_settings import BaseSettings
from pydantic import field_validator
import json


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    JWT_SECRET: str = "super_secret_key_change_in_prod"
    JWT_ALGORITHM: str = "HS256"
    API_KEY: str = "analytics_api_key_2026"
    API_TITLE: str = "Analytics Service - Burger eCommerce"
    API_VERSION: str = "1.0.0"

    CORS_ALLOWED_ORIGINS: str = "http://localhost:5173"

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()
settings = Settings()