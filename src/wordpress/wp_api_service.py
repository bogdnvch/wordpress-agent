import copy
import base64
import logging
import requests
from requests.exceptions import JSONDecodeError
from io import BytesIO
from typing import Optional

# from article import utils as article_utils
# from article.agent import generate_article
# from article.image_generation import ImageGenerator

from .config import wp_config
from . import utils


class WordpressApiService:
    """Uploads post or media to your Wordpress site."""

    def __init__(self):
        credentials: str = wp_config.WP_USER + ":" + wp_config.WP_PASSWORD
        self._token: bytes = base64.b64encode(credentials.encode())

    @property
    def _headers(self) -> dict:
        return {
            "Authorization": "Basic " + self._token.decode('utf-8')
        }

    @property
    def _media_headers(self) -> dict:
        media_headers = copy.deepcopy(self._headers)
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
            headers=self._headers,
            json={
                "title": title,
                "content": post,
                "status": "publish"
            }
        )
        return utils.wordpress_response_handler(response=response, action="upload", entity="post")

    def upload_image(self, image: BytesIO | None) -> Optional[int]:
        if not image:
            return
        response = requests.post(
            url=wp_config.WP_URL + "media",
            headers=self._media_headers,
            files={"file": ("image.jpg", image, 'image/jpeg')},
        )
        return utils.wordpress_response_handler(response=response, action="upload", entity="media")

    def update_post_with_media(self, post_id: int, media_id: int) -> Optional[int]:
        url = f"{self.wp_post_url}/{post_id}"
        response = requests.post(
            url=url,
            headers=self._headers,
            json={
                "featured_media": media_id
            }
        )
        return utils.wordpress_response_handler(response=response, action="update", entity="post")

    def fetch_all_posts(self):
        posts = []
        page = 1
        per_page = 10

        while True:
            response = requests.get(self.wp_post_url, params={"page": page, "per_page": per_page})
            if response.status_code != 200:
                break
            try:
                page_posts = response.json()
                if not page_posts:
                    break
                posts.extend(page_posts)
                logging.info(f"| Posts retrieved | count: {len(page_posts)} | page: {page} |")
            except JSONDecodeError:
                logging.error("Failed to retrieve posts from Wordpress")
                break
            page += 1
        return posts


# def make_post(query: str):
#     """Main function to make a post"""
#     wp_uploader = WordpressApiService()
#     post = generate_article(query=query)
#     if not article_utils.is_html(post):
#         logging.critical("Unfortunately post wasn't generated. Generated text is not HTML :( ")
#         logging.info(post)
#         return
#     title, post = article_utils.extract_title_from_content(content=post)
#     post_id = wp_uploader.upload_post(title=title, post=post)
#     image = ImageGenerator().generate(image_query=title)
#     media_id = wp_uploader.upload_image(image=image)
#     if post_id and media_id:
#         wp_uploader.update_post_with_media(post_id=post_id, media_id=media_id)
