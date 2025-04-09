from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from ..models import Book, Author, Category
from..serializers import BookSerializer
from datetime import datetime
from RAG.VectorStorage import VectorStorage

@api_view(["GET"])
def get_all_books(request):
    search = request.query_params.get("search")
    releaseFrom = request.query_params.get("releaseFrom")
    releaseTo = request.query_params.get("releaseTo")
    
    filters = Q()

    if search:
        filters &= (Q(title__icontains=search) |
                    Q(category__name__icontains=search) |
                    Q(author__name__icontains=search))
    
    if releaseFrom:
        try:
            release_date = datetime.strptime(releaseFrom, '%Y-%m-%d').date()
            filters &= Q(release__gte=release_date)
        except ValueError:
            return Response({"error": "Formato de fecha no válido. Use 'YYYY-MM-DD'."}, status=status.HTTP_400_BAD_REQUEST)
        
    if releaseTo:
        try:
            release_date = datetime.strptime(releaseTo, '%Y-%m-%d').date()
            filters &= Q(release__lte=release_date)
        except ValueError:
            return Response({"error": "Formato de fecha no válido. Use 'YYYY-MM-DD'."}, status=status.HTTP_400_BAD_REQUEST)
    
    books = Book.objects.filter(filters)

    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_book(request, id: int):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"})
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_related_books(request):
    query = request.query_params.get("query")
    if not query: return Response({"error": "Empty query param"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        vector_storage = VectorStorage()
        books = vector_storage.similarity_search(query)
        serializer = BookSerializer(books, many=True)
    except Exception:
        return Response(({"error": "Error getting related books"}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_book(request):
    book = BookSerializer(request.data)
    if not book.is_valid(): return Response(book.errors, status=status.HTTP_400_BAD_REQUEST)
    book.save()
    vector_storage = VectorStorage()
    vector_storage.add_book(book)
    return Response(book.data, status=status.HTTP_201_CREATED)

@api_view(["DELETE"])
def delete_book(request, id: int):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"})
    book.delete()
    return Response({"message": "Book deleted successfully"})

@api_view(["PATCH"])
def patch_book(request, id: int):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.data.get("title"):
        book.title = request.data.get("title")
    
    if request.data.get("description"):
        book.description = request.data.get("description")
    
    if request.data.get("release"):
        book.release = request.data.get("release")
    
    if request.data.get("cover"):
        book.cover = request.data.get("cover")

    if request.data.get("author"):
        try:
            new_authors = [Author.objects.get(id=a) for a in request.data.get("author")]
        except Author.DoesNotExist:
            return Response({"error": "Author(s) not found"}, status=status.HTTP_404_NOT_FOUND)
        
        book.author.set(new_authors) 

    if request.data.get("category"):
        try:
            new_categories = [Category.objects.get(id=c) for c in request.data.get("category")]
        except Category.DoesNotExist:
            return Response({"error": "Category(ies) not found"}, status=status.HTTP_404_NOT_FOUND)
        
        book.category.set(new_categories)

    if request.data.get("oneStarCount"):
        book.oneStarCount = request.data.get("oneStarCount")

    if request.data.get("twoStarCount"):
        book.twoStarCount = request.data.get("twoStarCount")

    if request.data.get("threeStarCount"):
        book.threeStarCount = request.data.get("threeStarCount")

    if request.data.get("fourStarCount"):
        book.fourStarCount = request.data.get("fourStarCount")

    if request.data.get("fiveStarCount"):
        book.fiveStarCount = request.data.get("fiveStarCount")

    book.save()
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)
