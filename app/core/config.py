from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    JWT_SECRET: str = "super_secret_key_change_in_prod"
    JWT_ALGORITHM: str = "HS256"
    API_KEY: str = "analytics_api_key_2026"
    API_TITLE: str = "Analytics Service - Burger eCommerce"
    API_VERSION: str = "1.0.0"

    model_config = {
        "env_file": ".env",
        "extra": "ignore"   # ← ESTA ES LA LÍNEA QUE FALTABA
    }


settings = Settings()
