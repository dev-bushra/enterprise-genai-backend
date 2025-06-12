# app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    AZURE_TENANT_ID: str
    AZURE_CLIENT_ID: str
    AZURE_CLIENT_SECRET: str
    AZURE_AUTHORITY: str = "https://login.microsoftonline.com"
    API_AUDIENCE: str  # your API App ID URI in Azure
    ALGORITHM: str = "RS256"

    class Config:
        env_file = ".env"

settings = Settings()
