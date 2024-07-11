import logging
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# ---------------------------------------------------- | config | ----------------------------------------------------

class ModelConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


class Settings(ModelConfig):
    SERPER_API_KEY: str = Field(..., env="SERPER_API_KEY")
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")


class WordpressSettings(ModelConfig):
    WP_USER: str = Field(..., env="WP_USER")
    WP_PASSWORD: str = Field(..., env="WP_PASSWORD")
    WP_URL: str = Field(..., env="WP_URL")


config = Settings(_env_file="../.env", _env_file_encoding='utf-8')
wp_config = WordpressSettings(_env_file="../.env", _env_file_encoding='utf-8')
print(wp_config.WP_URL)

# ---------------------------------------------------- | logger | ----------------------------------------------------

logging.basicConfig(level=logging.INFO)
