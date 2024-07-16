from typing import Optional

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic import Field
from pydantic_settings import BaseSettings
from pytz import utc


class TelegramSettings(BaseSettings):
    """Settings for Telegram."""

    TELEGRAM_API_TOKEN: str = Field(..., env="TELEGRAM_API_TOKEN")
    ASSISTANT_ID: Optional[str] = Field(None, env="ASSISTANT_ID")

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        extra = "ignore"


tg_config = TelegramSettings()
scheduler = AsyncIOScheduler(timezone=utc)
bot = Bot(token=tg_config.TELEGRAM_API_TOKEN)
dp = Dispatcher(bot=bot)
