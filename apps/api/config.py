"""Application configuration."""
import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./workey.db"
    api_secret_key: str = "dev_secret_key"
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    github_token: str = ""
    github_username: str = "wildhash"
    candidate_name: str = "Will Oak Wild"
    cors_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
