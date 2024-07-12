from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class WordpressSettings(BaseSettings):
    """Settings for Wordpress credentials and URL."""

    WP_USER: str = Field(..., env="WP_USER")
    WP_PASSWORD: str = Field(..., env="WP_PASSWORD")
    WP_URL: str = Field(..., env="WP_URL")

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


wp_config = WordpressSettings()
