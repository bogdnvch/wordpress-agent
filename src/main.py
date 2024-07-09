import json

from send_post import send_post
from image import generate_image
import requests
from config import wp_config
import base64
import copy
import openai
# if __name__ == "__main__":
#     query = "Напиши статью про Криштиану Роналду за июль 2024"
#     send_post(query=query)

# image_bytes = generate_image("криштиану роналду 2024")
credentials = wp_config.WP_USER + ":" + wp_config.WP_PASSWORD
token = base64.b64encode(credentials.encode())
headers = {"Authorization": "Basic " + token.decode("utf-8")}
media_headers = copy.deepcopy(headers)
media_headers.update({
    "Content-Disposition": f'attachment; filename="image.jpeg"',
    "Content-Type": "image/jpeg"
})
print(wp_config.WP_URL)
response = requests.post(
    wp_config.WP_URL + "media",
    headers=media_headers,
    files={"file": image_bytes},
    json={
        # "title": "gfjksdfgsdfgsdfgdsfgdsfgsddg;ld",
        # "content": "12312312312312",
        "status": "publish"
    })
print(response)


# credentials = wp_config.WP_USER + ":" + wp_config.WP_PASSWORD
# token = base64.b64encode(credentials.encode())
# headers = {"Authorization": "Basic " + token.decode('utf-8')}
# media_headers = copy.deepcopy(headers)
# media_headers.update({"Content-Disposition": f"attachment; filename=bullshit.jpg"})
# title = 'криштиану роналду за июль 2024'
# try:
#     image_bytes = generate_image(query=title)
#     response = requests.post("http://localhost/wp-json/wp/v2/media", headers=media_headers, files={"image": image_bytes})
#     print(response)
#     if response.status_code == 201:
#         print("Image uploaded successfully")
#     else:
#         print("Failed to upload image")
# except openai.BadRequestError as error:
#     if error.code == "content_policy_violation":
#         print("0(((0(")
