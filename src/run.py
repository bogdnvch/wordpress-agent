import logging
from wordpress.wp_uploader import make_post


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    query = "Мы IT компания, которая работает с искусственным интеллектом. Придумай какую-нибудь тему для статьи и сгенерируй статью."
    make_post(query=query)
