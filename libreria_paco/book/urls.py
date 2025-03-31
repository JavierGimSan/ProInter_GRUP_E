from django.urls import path
from .views.author import get_all_authors, get_author_books

urlpatterns = [
    path("/", get_all_authors, name="get_all_authors"),
    path("/<int:id>/books", get_author_books, name="get_author_books")
]