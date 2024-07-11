from datetime import datetime

import logging
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_core.tools import Tool

from serper import SerperService
from utils import clean_text


from config import config


# ------------------------------------------------- | article agent | -------------------------------------------------

class ArticleAgent:
    _model = "gpt-3.5-turbo"

    def initialize(self):
        return initialize_agent(
            tools=TOOLS,
            llm=self._llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            agent_kwargs=self._agent_kwargs,
            memory=self._memory
        )

    @property
    def _llm(self):
        return ChatOpenAI(temperature=0, model=self._model, openai_api_key=config.OPENAI_API_KEY)

    @property
    def _agent_kwargs(self):
        return {
            "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
            "system_message": self._system_message
        }

    @property
    def _system_message(self):
        with open("agent_prompt.txt", "r", encoding="utf-8") as file:
            content = file.read()
        return SystemMessage(
            content=content
        )

    @property
    def _memory(self):
        return ConversationSummaryBufferMemory(
            memory_key="memory",
            return_messages=True,
            llm=self._llm,
            max_tokens_limit=1000
        )

# -------------------------------------------------- | agent tools | --------------------------------------------------


def search(query: str, *args, **kwargs) -> str:
    response_data = SerperService().request_to_serper(query=query)
    urls = [result["link"] for result in response_data["organic"]]
    logging.info("Found 10 websites:\n")
    [
        logging.info(f"\t{url}")
        for url in urls
    ]
    return str(urls)


def scrape_website(url: str, *args, **kwargs) -> str:
    loader = UnstructuredURLLoader(urls=[url])
    content = loader.load()
    if not content or not content[0]:
        return "content_error"
    print("text before cleaning: ", len(content[0].page_content))
    text = clean_text(content[0].page_content)
    print("text after cleaning: ", len(text))
    return text


def get_current_datetime(*args, **kwargs):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time


TOOLS = [
    Tool(
        name="search",
        func=search,
        description="Useful when you need to find a website. This function returns 10 urls. ",
    ),
    Tool(
        name="scrape_website",
        func=scrape_website,
        description="Useful when you need to get content from the website url. "
                    "If return 'content_error' try another url."
    ),
    Tool(
        name="get_current_datetime",
        func=get_current_datetime,
        description="Useful when you need to get current date or time."
    )
]
