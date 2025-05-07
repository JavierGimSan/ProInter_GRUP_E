from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from RAG.VectorStorage import VectorStorage
from RAG.factory import llm_factory
from libreria_paco.settings import LLM_MODEL, OLLAMA_SERVER
from ..serializers import BookSerializer


@api_view(["GET"])
def query(request):
    query = request.query_params.get("query")
    if not query: return Response({"error": "Query param not set"})
    vector_storage = VectorStorage()
    llm = llm_factory.get()

    template = """
    A partir de la información de este libo responde la siguiente consulta.
    Si la consulta no tiene ralación con la información, responde sin tener en cuenta la información.
    Información: {info}
    Consulta: {query}
    """
    [book] = vector_storage.similarity_search(query, k=1)
    inputs = {
        "info": book.detailed_str(),
        "query": query
    }

    response = llm.query_with_template(template, inputs)
    serializer = BookSerializer(book)
    return Response({"message": response, "book":serializer.data}, status=status.HTTP_200_OK)