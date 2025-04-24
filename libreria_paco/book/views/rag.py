from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from RAG.VectorStorage import VectorStorage
from RAG.models.LLM import LLM
from libreria_paco.settings import LLM_MODEL, OLLAMA_SERVER
from ..serializers import BookSerializer


@api_view(["GET"])
def query(request):
    query = request.query_params.get("query")
    if not query: return Response({"error": "Query param not set"})
    vector_storage = VectorStorage()
    llm = LLM(model=LLM_MODEL, base_url=OLLAMA_SERVER)

    template = """
    A partir de la información de este libo responde la siguiente consulta.
    Información: {info}
    Consulta: {query}
    """
    [book] = vector_storage.similarity_search(query, k=1)
    inputs = {
        "info": book,
        "query": query
    }

    response = llm.query_with_template(template, inputs)
    serializer = BookSerializer(book)
    return Response({"message": response, "book":serializer.data})