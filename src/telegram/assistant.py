from typing import Optional

from openai import Client

from article.config import config as article_config
from .config import tg_config
from wordpress.wp_api_service import WordpressApiService

client = Client(api_key=article_config.OPENAI_API_KEY)


def generate_title(assistant_id: str, thread_id: str) -> Optional[str]:
    query = get_title_prompt()
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=query
    )
    run = client.beta.threads.runs.create_and_poll(
        model="gpt-4-turbo",
        thread_id=thread_id,
        assistant_id=assistant_id,
        poll_interval_ms=1000
    )
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        text = messages.data[0].content[0].text
        new_message = text.value
        return new_message
    return None


def get_or_create_assistant():
    instructions = ("All conversation in Russian. We are an IT company that works with artificial intelligence. "
                    "Generate an interesting topic for the article. You should recognize whether user likes the topic or not"
                    "If not, keep suggesting other topics until user likes it. if user likes the topic, call function `define_whether_user_likes_article_topic`")
    if tg_config.ASSISTANT_ID:
        assistant = client.beta.assistants.retrieve(assistant_id=tg_config.ASSISTANT_ID)
    else:
        assistant = client.beta.assistants.create(
            name="Title Creator",
            instructions=instructions,
            model="gpt-4-turbo",
            tools=[{
                "type": "function",
                "function": func
            }],
        )
    return assistant


func = {
    "name": "define_whether_user_likes_article_topic",
    "description": "Return the topic if user likes",
    "parameters": {
        "type": "object",
        "properties": {
            "topic_that_user_likes": {
                "type": "string",
                "description": "The topic that the user likes",
            }
        },
        "required": ["topic_that_user_likes"]
    }
}


def get_title_prompt():
    query = "Generate a title. Don't repeat existing topics. Here are the published articles:"
    wp = WordpressApiService()
    posts = wp.fetch_all_posts()
    titles = [f"-{post['title']['rendered']}" for post in posts]
    titles = "\n".join(titles)
    return query + titles
