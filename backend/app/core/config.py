from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    secret_key: str = "unsafe-development-secret-change-me"
    database_url: str = "sqlite:///./vorbis.db"
    upload_dir: str = "./data/uploads"
    max_upload_mb: int = 200
    access_token_minutes: int = 60
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
