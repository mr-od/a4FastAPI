from pydantic import BaseSettings
from functools import lru_cache
from pathlib import Path
import os

IMAGES_DIR = f'{Path(__file__).resolve().parent.joinpath("images")}'


class Settings(BaseSettings):
    # database
    postgres_user: str
    postgres_password: str
    postgres_server: str
    postgres_port: int
    postgres_database_name: str
    database_url: str
    project_name: str
    project_version: str

    # jwt
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 1000

    bucket_name: str = os.getenv('BUCKET', 'afia4')
    oss_access_key_id: str
    oss_secret_access_key: str
    oss_endpoint: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> Settings:
    return Settings()
