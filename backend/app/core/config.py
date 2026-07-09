"""
Central application settings.
All config values are read from environment variables (.env locally,
real env vars on Render/Vercel). Never hardcode secrets here.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "HackMate API"
    ENV: str = "development"  # development | production

    # --- Database ---
    # Postgres, matching production (Render). Override via .env locally —
    # e.g. if you run Postgres in Docker: postgresql://postgres:Shre123@localhost:5432/Hackmate
    DATABASE_URL: str = "postgresql://postgres:Rockon07@localhost:5432/HackMate"

    # --- Auth (placeholders until Person A's real Auth module lands) ---
    JWT_SECRET: str = "dev-only-secret-change-me"
    JWT_ALGORITHM: str = "HS256"

    # --- CORS ---
    CORS_ORIGINS: list[str] = ["http://localhost:5432"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
