import asyncio
import logging

from telegram.config import scheduler, dp, bot
from telegram.handlers import register_handlers
from telegram.jobs import generate_title_job

logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.INFO)


async def start_bot():
    register_handlers(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    scheduler.start()
    scheduler.add_job(generate_title_job, "cron", id="get_title", hour=7, minute=7)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
