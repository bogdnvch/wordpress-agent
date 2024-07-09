from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERPER_API_KEY: str = Field(..., env="SERPER_API_KEY")
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")

    # model_config = SettingsConfigDict(env_file='.env.localhost', env_file_encoding='utf-8', extra="ignore")

    class Config:
        extra = "ignore"
        env_file = ".env.localhost"


class WordpressSettings(BaseSettings):
    WP_USER: str = Field(..., env="WP_USER")
    WP_PASSWORD: str = Field(..., env="WP_PASSWORD")
    WP_URL: str = Field(..., env="WP_URL")

    # model_config = SettingsConfigDict(env_file='.env.localhost', env_file_encoding='utf-8', extra="ignore")

    class Config:
        extra = "ignore"
        env_file = ".env.localhost"


config = Settings()
wp_config = WordpressSettings()
