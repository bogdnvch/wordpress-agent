from langchain import PromptTemplate, LLMChain
from langchain_openai import ChatOpenAI


class ArticlePickerService:
    _model = "gpt-3.5-turbo"
    _prompt_template = """
    You are a world class journalist and researcher,
    you are extremely good ad find most relevant articles to certain topic;
    {response_str}
    Above is the list of search results for the query {query}.
    Please choose the best article from the list, return ONLY url, don't include anything else;
    """

    def __init__(self, response_data, query):
        self._response_data = str(response_data)
        self._query = query

    def run(self) -> str:
        article_picker_chain = self._get_chain()
        url = article_picker_chain.predict(response_str=self._response_data, query=self._query)
        return url

    def _get_chain(self):
        prompt = self._get_prompt()
        llm = ChatOpenAI(model_name=self._model)
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain

    def _get_prompt(self):
        prompt = PromptTemplate(input_varialbles=["response_str", "query"], template=self._prompt_template)
        return prompt
