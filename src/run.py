import logging
from wordpress.wp_uploader import make_post


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    query = "Напиши новости про спорт 2024 года"
    make_post(query=query)
    # print("dfglkujdfg")