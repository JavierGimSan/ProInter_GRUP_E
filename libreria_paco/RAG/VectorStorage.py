from .models.Embedding import Embedding
from langchain_chroma import Chroma
from langchain_core.documents import Document
import sys, os, django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "libreria_paco.settings")
django.setup()

from book.models import Book
from libreria_paco.settings import VECTOR_STORAGE, EMBEDDING_MODEL, OLLAMA_SERVER

class VectorStorage:

    def __init__(self):
        self.embedding_model = Embedding(model=EMBEDDING_MODEL, base_url=OLLAMA_SERVER)
        self.vector_storage = Chroma(
            collection_name="book",
            embedding_function=self.embedding_model.model,
            persist_directory=str(VECTOR_STORAGE)
        )

    def add_book(self, book: Book):
        document = Document(
            page_content=book.__str__(),
            metadata={"id": book.id}
        )

        self.vector_storage.add_documents([document])

    def add_books(self, books: list[Book]):
        documents = []
        for book in books:
            document = Document(
                page_content=book.detailed_str(),
                metadata={"id": book.id}
            )
            documents.append(document)

        self.vector_storage.add_documents(documents)

    def similarity_search(self, query: str, k: int = 10):
        res = self.vector_storage.similarity_search(query=query, k=k)

        books = [Book.objects.get(id=book.metadata["id"]) for book in res]
        return books
        