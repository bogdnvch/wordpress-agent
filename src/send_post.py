import copy
import base64
import logging
import requests
from io import BytesIO
from typing import Optional

from bs4 import BeautifulSoup
from langchain_community.callbacks import get_openai_callback

import image
import utils
from config import wp_config
from agent import ArticleAgent


# --------------------------------------------- | wordpress upload data | ---------------------------------------------

class WordpressUploader:
    """Uploads post or media to your Wordpress site."""

    def __init__(self):
        credentials: str = wp_config.WP_USER + ":" + wp_config.WP_PASSWORD
        self._token: bytes = base64.b64encode(credentials.encode())

    @property
    def headers(self) -> dict:
        return {
            "Authorization": "Basic " + self._token.decode('utf-8')
        }

    @property
    def media_headers(self) -> dict:
        media_headers = copy.deepcopy(self.headers)
        media_headers.update({"Content-Disposition": f"attachment; filename=image.jpg"})
        return media_headers

    @property
    def wp_post_url(self) -> str:
        return wp_config.WP_URL + "posts"

    @property
    def wp_media_url(self) -> str:
        return wp_config.WP_URL + "media"

    def upload_post(self, title: str, post: str) -> Optional[int]:
        response = requests.post(
            self.wp_post_url,
            headers=self.headers,
            json={
                "title": title,
                "content": post,
                "status": "publish"
            }
        )
        return utils.response_handler(response=response, action="upload", entity="post")

    def upload_image(self, image_bytes: BytesIO | None) -> Optional[int]:
        if not image_bytes:
            return
        response = requests.post(
            url=wp_config.WP_URL + "media",
            headers=self.media_headers,
            files={"file": ("image.jpg", image_bytes, 'image/jpeg')},
        )
        return utils.response_handler(response=response, action="upload", entity="media")

    def update_post_with_media(self, post_id: int, media_id: int) -> Optional[int]:
        url = f"{self.wp_post_url}/{post_id}"
        response = requests.post(
            url=url,
            headers=self.headers,
            json={
                "featured_media": media_id
            }
        )
        return utils.response_handler(response=response, action="update", entity="post")


def get_generated_post(query: str) -> str:
    """Gets generated post"""
    agent = ArticleAgent().initialize()
    with get_openai_callback() as cb:
        output = agent({"input": query})
        print(cb)
    return output["output"]


def extract_title_from_content(content: str) -> tuple[str, str]:
    """Extracts title post content"""
    soup = BeautifulSoup(content, "html.parser")
    title = soup.find("h1").text
    content = content.replace(title, "")
    return title, content


def is_html(text: str) -> bool:
    """Checks if text is HTML"""
    soup = BeautifulSoup(text, "html.parser")
    return bool(soup.find())


# -------------------------------------------------- | make a post | --------------------------------------------------

def make_post(query: str):
    """Main function to make a post"""
    wp_uploader = WordpressUploader()
    post = get_generated_post(query=query)
    if not is_html(post):
        logging.critical("Unfortunately post wasn't generated. Generated text is not HTML :( ")
        return
    title, post = extract_title_from_content(content=post)
    post_id = wp_uploader.upload_post(title=title, post=post)
    image_bytes = image.get_generated_image(image_query=title)
    media_id = wp_uploader.upload_image(image_bytes=image_bytes)
    if post_id and media_id:
        wp_uploader.update_post_with_media(post_id=post_id, media_id=media_id)
