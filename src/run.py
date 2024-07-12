import logging
from wordpress.wp_uploader import make_post


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    query = "Напиши новости про IT за 2024 год"
    make_post(query=query)
