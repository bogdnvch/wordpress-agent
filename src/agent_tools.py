from bs4 import BeautifulSoup
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_core.tools import Tool

from article_picker import ArticlePickerService
from serper import SerperService
from utils import clean_text


def search(query):
    response_data = SerperService().request_to_serper(query=query)
    best_article_url = ArticlePickerService(query=query, response_data=response_data["organic"]).run()
    return best_article_url


def scrape_website(url: str) -> str:
    loader = UnstructuredURLLoader(urls=[url])
    content = loader.load()
    soup = BeautifulSoup(content[0].page_content, "html.parser")
    text = soup.get_text()
    text = clean_text(text)
    return text


TOOLS = [
    Tool(
        name="search",
        func=search,
        description="Useful when you need to find a website",
    ),
    Tool(
        name="scrape_website",
        func=scrape_website,
        description="Useful when you need to get content from the website url"
    )
]
