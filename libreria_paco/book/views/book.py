from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from ..models import Book, Author, Category
from..serializers import BookSerializer, BookWriteSerializer
from datetime import datetime
from RAG.VectorStorage import VectorStorage
from django.conf import settings
from django.db.models import Q
from datetime import datetime
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from uuid import uuid4
import os

@api_view(["GET"])
def get_all_books(request):
    search = request.query_params.get("search")
    releaseFrom = request.query_params.get("releaseFrom")
    releaseTo = request.query_params.get("releaseTo")
    categories = request.query_params.get("category")
    priceFrom = request.query_params.get("priceFrom")
    priceTo = request.query_params.get("priceTo")
    starsFrom = request.query_params.get("starsFrom")
    starsTo = request.query_params.get("starsTo")
    
    filters = Q()

    if search:
        filters &= (Q(title__icontains=search) |
                    Q(category__name__icontains=search) |
                    Q(author__name__icontains=search))
    
    if categories:
        try:
            category_ids = [int(cid) for cid in categories.split(',') if cid.strip().isdigit()]
            filters &= Q(category__id__in=category_ids)
        except ValueError:
            return Response({"error": "Los IDs de categoría deben ser enteros separados por comas."}, status=status.HTTP_400_BAD_REQUEST)

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

    if priceFrom:
        try:
            filters &= Q(price__gte=int(priceFrom))
        except ValueError:
            return Response({"error": "El parámetro 'priceFrom' debe ser un número."}, status=status.HTTP_400_BAD_REQUEST)

    if priceTo:
        try:
            filters &= Q(price__lte=int(priceTo))
        except ValueError:
            return Response({"error": "El parámetro 'priceTo' debe ser un número."}, status=status.HTTP_400_BAD_REQUEST)

    books = Book.objects.filter(filters).distinct()

    try:
        stars_from = float(starsFrom) if starsFrom else None
        stars_to = float(starsTo) if starsTo else None
    except ValueError:
        return Response({"error": "Los parámetros 'starsFrom' y 'starsTo' deben ser números."}, status=status.HTTP_400_BAD_REQUEST)

    if stars_from is not None:
        books = [book for book in books if book.stars >= stars_from]

    if stars_to is not None:
        books = [book for book in books if book.stars <= stars_to]

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

@api_view(["GET"])
def get_top_books(request):
    limit = request.query_params.get("limit")
    if limit: limit = int(limit) 
    else: limit = 20
    books = list(Book.objects.all())
    books.sort(key=lambda book: book.stars, reverse=True)
    top_books = books[:limit]
    serializer = BookSerializer(top_books, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def create_book(request):
    cover_file = request.FILES.get("cover")
    mutable_data = request.data.copy()

    if cover_file:
        file_name = f"{uuid4()}_{cover_file.name}"
        cover_path = os.path.join("uploads", file_name)
        full_path = os.path.join(settings.MEDIA_ROOT, cover_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb+") as destination:
            for chunk in cover_file.chunks():
                destination.write(chunk)

        cover_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, cover_path))
        mutable_data["cover"] = cover_url

    serializer = BookWriteSerializer(data=mutable_data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    book = serializer.save()
    vector_storage = VectorStorage()
    vector_storage.add_book(book)

    read_serializer = BookSerializer(book)
    return Response(read_serializer.data, status=status.HTTP_201_CREATED)

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

@api_view(["GET"])
def vote_one_star(request, id: int):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    
    book.oneStarCount += 1
    book.save()
    return Response({"message": "Book updated"})

@api_view(["GET"])
def vote_two_star(request, id: int):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    
    book.twoStarCount += 1
    book.save()
    return Response({"message": "Book updated"})

@api_view(["GET"])
def vote_three_star(request, id: int):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    
    book.threeStarCount += 1
    book.save()
    return Response({"message": "Book updated"})

@api_view(["GET"])
def vote_four_star(request, id: int):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    
    book.fourStarCount += 1
    book.save()
    return Response({"message": "Book updated"})

@api_view(["GET"])
def vote_five_star(request, id: int):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    
    book.fiveStarCount += 1
    book.save()
    return Response({"message": "Book updated"})