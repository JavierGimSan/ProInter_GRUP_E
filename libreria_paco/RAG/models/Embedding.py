from langchain_ollama import OllamaEmbeddings

class Embedding:

    def __init__(self, model: str, base_url: str):
        self.model = OllamaEmbeddings(
            model= model,
            base_url=base_url
        )