from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsModel(BaseSettings):

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    tg_api_token: str = Field(..., alias='TG_API_TOKEN')
    db_name: str = Field(..., alias='DB_NAME')
    db_user: str = Field(..., alias='DB_USER')
    db_password: str = Field(..., alias='DB_PASSWORD')
    db_host: str = Field(..., alias='DB_HOST')
