import base64
import copy

import requests

from bs4 import BeautifulSoup
from langchain_community.callbacks import get_openai_callback

from agent import ArticleAgent
from config import wp_config
from image import generate_image


def get_content(query: str):
    agent = ArticleAgent().initialize()
    with get_openai_callback() as cb:
        output = agent({"input": query})
        print(cb)
    return output["output"]


def extract_title_from_content(content: str) -> tuple[str, str]:
    soup = BeautifulSoup(content, "html.parser")
    title = soup.find("h1").text
    content = content.replace(title, "")
    return title, content


def send_post(query: str):
    credentials = wp_config.WP_USER + ":" + wp_config.WP_PASSWORD
    token = base64.b64encode(credentials.encode())
    headers = {"Authorization": "Basic " + token.decode('utf-8')}

    media_headers = copy.deepcopy(headers)
    media_headers.update({"Content-Disposition": f"attachment; filename=bullshit.jpg"})

    article = get_content(query=query)
    title, article = extract_title_from_content(content=article)
    image_bytes = generate_image(query=title)
    response = requests.post(wp_config.WP_URL + "media", headers=media_headers, files={"file": image_bytes})
    if response.status_code == 201:
        print("Image uploaded successfully")
    else:
        print("Failed to upload image")

    post = {
        "title": title,
        "content": article,
        "status": "publish",
    }

    response = requests.post(wp_config.WP_URL + "posts", headers=headers, json=post)
    print(response)
    if response.status_code == 201:
        print("Post uploaded successfully")
    else:
        print("Failed to upload post")
