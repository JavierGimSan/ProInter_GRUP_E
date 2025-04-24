from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

class LLM:

    def __init__(self, model: str, base_url: str):
        self.model = OllamaLLM(
            model=model,
            base_url=base_url
        )

    def query_with_template(self, template: str, inputs: dict):
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.model
        return chain.invoke(inputs)