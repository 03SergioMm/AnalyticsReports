from pydantic_settings import BaseSettings
from pydantic import field_validator
import json


class Settings(BaseSettings):
    DB_URL: str
    JWT_SECRET: str = "super_secret_key_change_in_prod"
    JWT_ALGORITHM: str = "HS256"
    API_KEY: str = "analytics_api_key_2026"
    API_TITLE: str = "Analytics Service - Burger eCommerce"
    API_VERSION: str = "1.0.0"

    CORS_ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]

    @field_validator("CORS_ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)      # maneja: ["http://..."]
            except (json.JSONDecodeError, ValueError):
                return [o.strip() for o in v.split(",") if o.strip()]  # maneja: http://...,http://...
        return v

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()