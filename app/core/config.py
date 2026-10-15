from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    geo_primary_url: str = "https://ip-api.com/json"
    geo_fallback_url: str = "https://ipapi.co/json"
    notification_mode: str = "console"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
