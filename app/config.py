from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings and configurations are read from this file.
    This file is responsible for reading the .env file.
    """
    app_name: str = "Doc-Search"
    gcp_service_account_path: str
    gcp_storage_bucket_name: str
    signed_url_expiry_time: int = 15  # 15 minutes
    cors_origins: str
    SQLALCHEMY_DATABASE_URL: str
    VOYAGE_AI_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
