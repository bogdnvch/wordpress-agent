import asyncio
import json

from aiogram import Dispatcher, Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from openai import Client

from article.config import config
from storage.storage import user_storage, save_users
from telegram.config import scheduler
from telegram.states import UserInfo
from telegram.assistant import get_or_create_assistant
from telegram.jobs import generate_article_job

router = Router()
client = Client(api_key=config.OPENAI_API_KEY)


@router.message(Command("start"))
async def handle_start(message: types.Message, state: FSMContext):
    await state.set_state(UserInfo.thread_id)
    user_data = {
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "chat_id": message.chat.id
    }
    save_users({message.from_user.id: user_data})
    await message.answer("Hi, I’m your personal copywriter, will help you write articles on your website")


@router.message(lambda message: message.text)
async def handle_text(message: types.Message):
    thread_id = user_storage[str(message.from_user.id)]["thread_id"]
    assistant = get_or_create_assistant()
    print(assistant.id)
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message.text
    )
    run = client.beta.threads.runs.create_and_poll(
        model="gpt-4-turbo",
        thread_id=thread_id,
        assistant_id=assistant.id,
        poll_interval_ms=1000
    )
    new_message = ":((("
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        text = messages.data[0].content[0].text
        new_message = text.value
    elif run.status == "requires_action":
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        tool_outputs = list(map(get_output_from_tool_call, tool_calls))
        title = tool_outputs[0]["output"]
        run = client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            text = messages.data[0].content[0].text
            new_message = text.value
            scheduler.remove_job(job_id="gen_article")
            await asyncio.to_thread(generate_article_job, title)
    await message.answer(new_message)


def get_output_from_tool_call(tool_call) -> dict:
    value = json.loads(tool_call.function.arguments)["topic_that_user_likes"]
    return {
        "tool_call_id": tool_call.id,
        "output": value
    }


def register_handlers(dp: Dispatcher):
    dp.include_router(router)
