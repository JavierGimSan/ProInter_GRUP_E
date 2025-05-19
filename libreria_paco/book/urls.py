from django.urls import path
from .views import author, category, book, rag

author_urls = [
    path("authors/", author.get_all_authors, name="get_all_authors"),
    path("authors/<int:id>/", author.get_author, name="get_author"),
    path("authors/<int:id>/books/", author.get_author_books, name="get_author_books"),
    path("authors/create/", author.create_author, name="create_author"),
    path("authors/<int:id>/delete/", author.delete_author, name="delete_author"),
    path("authors/<int:id>/update/", author.patch_author, name="patch_author"),
]

category_urls = [
    path("categories/", category.get_all_categories, name="get_all_categories"),
    path("categories/create/", category.create_category, name="create_category"),
    path("categories/<int:id>/delete", category.delete_category, name="delete_category"),
    path("categories/<int:id>/update", category.patch_category, name="patch_author")
]

book_urls = [
    path("books/", book.get_all_books, name="get_all_books"),
    path("books/<int:id>/", book.get_book, name="get_book"),
    path("books/top", book.get_top_books, name="get_top_books"),
    path("books/related", book.get_related_books, name="get_ralated_books"),
    path("books/create", book.create_book, name="create_book"),
    path("books/<int:id>/delete", book.delete_book, name="delete_book"),
    path("books/<int:id>/update", book.patch_book, name="patch_book")
]

rag_urls = [
    path("chat/", rag.query, name="chat_query")
]

urlpatterns = author_urls + category_urls + book_urls + rag_urls