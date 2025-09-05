from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):



     class Config:
          env_config = SettingsConfigDict(
                  env_file='.env',
                  env_file_encoding='utf-8'
          )
