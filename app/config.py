from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "DashFlow"

    database_url: str


    #jwt
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080

    gemini_api_key: str = ""

    google_ads_client_id: str = ""
    google_ads_client_secret: str = ""
    google_ads_developer_token: str = ""

    meta_app_id: str = ""
    meta_app_secret: str = ""

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()