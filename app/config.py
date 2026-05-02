from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings and configurations are read from this file.
    This file is responsible for reading the .env file.
    """

    APP_NAME: str = "Doc-Search"
    GCP_SERVICE_ACCOUNT_PATH: str
    GCP_STORAGE_BUCKET_NAME: str
    SIGNED_URL_EXPIRY_TIME: int = 15  # 15 minutes
    CORS_ORIGINS: str
    SQLALCHEMY_DATABASE_URL: str
    VOYAGE_AI_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
