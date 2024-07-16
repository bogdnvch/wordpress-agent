from wordpress.wp_api_service import WordpressApiService

query = """
We are an IT company that works with artificial intelligence. Generate an interesting topic for the article.
Do not repeat existing article titles. Choose another topic.

Here are the published articles:
"""


def get_title_query():
    wp = WordpressApiService()
    posts = wp.fetch_all_posts()
    titles = [f"-{post['title']['rendered']}" for post in posts]
    titles = "\n".join(titles)
    return query + titles
