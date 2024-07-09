from io import BytesIO
import requests

from openai import OpenAI

from config import config


def generate_image(query: str) -> BytesIO:
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    response = client.images.generate(
        model="dall-e-3",
        prompt=query,
        size="1792x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    response = requests.get(image_url)
    response.raise_for_status()
    image_bytes = BytesIO(response.content)
    return image_bytes
