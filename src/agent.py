from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_openai import ChatOpenAI

import agent_tools


class ArticleAgent:
    _model = "gpt-3.5-turbo"

    def initialize(self):
        return initialize_agent(
            tools=agent_tools.TOOLS,
            llm=self._llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            agent_kwargs=self._agent_kwargs,
            memory=self._memory
        )

    @property
    def _llm(self):
        return ChatOpenAI(temperature=0, model=self._model)

    @property
    def _agent_kwargs(self):
        return {
            "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
            "system_message": self._system_message
        }

    @property
    def _system_message(self):
        with open("src/agent_prompt.txt", "r", encoding="utf-8") as file:
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

