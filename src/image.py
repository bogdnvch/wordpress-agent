from io import BytesIO
import requests
from typing import Optional

import logging
from openai import OpenAI, BadRequestError
from PIL import Image

from config import config

# ----------------------------------- | image generating and helpful functions | -----------------------------------


def get_generated_image(image_query: str, max_retries=5) -> Optional[BytesIO]:
    """Generates an image for post"""
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    for num in range(max_retries):
        image_query = rephrase_image_query(previous_image_query=image_query)
        logging.info(f"Image query: {image_query}")
        try:
            logging.info(f"Generating image try №{num+1}")
            response = client.images.generate(
                model="dall-e-3",
                prompt=image_query,
                size="1792x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            response = requests.get(image_url)
            response.raise_for_status()
            image_bytes = BytesIO(response.content)
            image_bytes.seek(0)
            image_bytes = compress_image(image_bytes=image_bytes, max_size_mb=2.0)
            return image_bytes
        except BadRequestError as error:
            if error.code == "content_policy_violation":
                logging.error("'content_policy_violation' error while generating image")
            else:
                logging.error(error)
    logging.error("Image generation failed :(")


def rephrase_image_query(previous_image_query: str):
    """Rephrases the image query for avoiding content policies"""
    prompt = f"""
    Please rephrase the following previous image query to be neutral and suitable for generating an image,
    and translate it to English. Also new query should avoid 'content_policy_violation'.
    Avoid any content that may be considered inappropriate or offensive, 
    ensuring the image aligns with content policies.
    This is previous image query: '{previous_image_query}'
    """

    client = OpenAI(api_key=config.OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt}
        ],
        max_tokens=100,
        n=1,
    )
    rephrased_query = response.choices[0].message.content
    return rephrased_query


def compress_image(image_bytes: BytesIO, max_size_mb: float) -> BytesIO:
    """Compress the image, because the Wordpress maximum size of media file is 2MB"""
    image = Image.open(image_bytes)
    output = BytesIO()
    quality = 95
    while True:
        output.seek(0)
        image.save(output, format='JPEG', quality=quality)
        size_mb = output.tell() / (1024 * 1024)
        if size_mb <= max_size_mb or quality <= 10:
            break
        quality -= 5
    output.seek(0)
    return output
