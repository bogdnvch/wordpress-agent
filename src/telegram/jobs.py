import asyncio
from datetime import datetime, timedelta
import logging

from openai import Client

from article.agent import generate_article
from article import utils as article_utils
from article.image_generation import ImageGenerator
from article.config import config
from storage.storage import user_storage, save_users
from telegram.assistant import get_or_create_assistant, generate_title
from telegram.config import tg_config, bot, scheduler
from wordpress.wp_api_service import WordpressApiService


client = Client(api_key=config.OPENAI_API_KEY)


def generate_article_job(title: str):
    post = generate_article(topic=title)
    wp_uploader = WordpressApiService()
    if not article_utils.is_html(post):
        logging.critical("Unfortunately post wasn't generated. Generated text is not HTML :( ")
        logging.info(post)
        return
    post_id = wp_uploader.upload_post(title=title, post=post)
    image = ImageGenerator().generate(image_query=title)
    media_id = wp_uploader.upload_image(image=image)
    if post_id and media_id:
        wp_uploader.update_post_with_media(post_id=post_id, media_id=media_id)


async def generate_title_job():
    assistant = get_or_create_assistant()
    thread = client.beta.threads.create()
    users = {
        tg_config.USER_ID: {
            "thread_id": thread.id
        }
    }
    save_users(users)
    title = await asyncio.to_thread(generate_title, assistant.id, thread.id)
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="assistant",
        content=f"Вот моя предложенная статья. {title}. Как вам?"
    )
    print(title)
    print(22, thread.id)
    await bot.send_message(chat_id=tg_config.USER_ID, text=title)
    hour, minute = get_time_plus_30_minutes()
    scheduler.add_job(generate_article_job, "cron", args=[title], id="gen_article", hour=hour, minute=minute)


def get_time_plus_30_minutes():
    current_time = datetime.now()
    new_time = current_time + timedelta(minutes=30)
    hour = new_time.hour
    minute = new_time.minute
    return hour, minute

