from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

class LLM:

    def __init__(self, model):
        self.model = model

    def query_with_template(self, template: str, inputs: dict):
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.model
        res = chain.invoke(inputs)
        return res if type(res) == str else res.content