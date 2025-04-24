from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Author
from ..serializers import AuthorSerializer, BookSerializer

@api_view(["GET"])
def get_all_authors(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_author(request, id: int):
    try:
        author = Author.objects.get(id=id)
    except Author.DoesNotExist:
        return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = AuthorSerializer(author)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_author_books(request, id: int):
    try:
        author = Author.objects.get(id=id)
    except Author.DoesNotExist:
        return Response({"error": "Author not found"})
    
    books = author.books.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_author(request):
    serializer = AuthorSerializer(request.data)
    if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["DELETE"])
def delete_author(request, id: int):
    try:
        author = Author.objects.get(id=id)
    except Author.DoesNotExist:
        return Response({"error": "Author not found"})
    
    author.delete()
    return Response({"message": "Author deleted successfully"})

@api_view(["PATCH"])
def patch_author(request, id: int):
    try:
        author = Author.objects.get(id)
    except Author.DoesNotExist:
        return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
    
    new_name = request.data.get("name", None)
    if not new_name: return Response({"error": "name not set"}, status=status.HTTP_400_BAD_REQUEST)

    author.name = new_name
    author.save()
    serializer = AuthorSerializer(author)
    return Response(serializer.data, status=status.HTTP_200_OK)