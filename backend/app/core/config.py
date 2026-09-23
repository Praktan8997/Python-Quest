import os
from dotenv import load_dotenv

# Load .env file for local development
# In production (Render), env vars are injected directly — load_dotenv is a no-op
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Python Quest"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    # Database — defaults to SQLite for local dev; Render injects PostgreSQL URL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./python_quest.db")

    # Auth Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_key_change_in_production_12345")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super_secret_jwt_key_python_quest_2026")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # CORS — comma-separated list of allowed origins
    @property
    def CORS_ORIGINS(self) -> list:
        raw = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
        return [o.strip() for o in raw.split(",") if o.strip()]

    # Execution Service
    CODE_EXECUTION_URL: str = os.getenv("CODE_EXECUTION_URL", "http://127.0.0.1:8001/run")


settings = Settings()
