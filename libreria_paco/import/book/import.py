import os, sys
import pandas
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "libreria_paco.settings")
django.setup()

from book.models import Author, Category, Book
from RAG.VectorStorage import VectorStorage

AUTHOR_CSV = "import/book/author.csv"
CATEGORY_CSV = "import/book/category.csv"
BOOK_CSV = "import/book/book.csv"


def import_authors():
    csv = pandas.read_csv(AUTHOR_CSV)
    names = csv["name"].to_list()
    
    for name in names:
        author = Author(name=name)
        author.save()

def import_categories():
    csv = pandas.read_csv(CATEGORY_CSV)
    names = csv["name"].to_list()

    for name in names:
        author = Category(name=name)
        author.save()

def import_book():
    csv = pandas.read_csv(BOOK_CSV)
    
    books = []
    for idx, row in csv.iterrows():
        book = Book(
            title=row["title"],
            description=row["description"],
            release=row["release"],
            cover=row["cover"],
            price=row.get("price"),
            oneStarCount=row.get("oneStarCount", 0),
            twoStarCount=row.get("twoStarCount", 0),
            threeStarCount=row.get("threeStarCount", 0),
            fourStarCount=row.get("fourStarCount", 0),
            fiveStarCount=row.get("fiveStarCount", 0),
        )
        book.save()
        author_ids = row["author_ids"].split("|")
        book.author.set(Author.objects.filter(id__in=author_ids))

        category_ids = row["category_ids"].split("|")
        book.category.set(Category.objects.filter(id__in=category_ids))
        
        books.append(book)

    vector_storage = VectorStorage()
    vector_storage.add_books(books)

if __name__ == "__main__":
    validArgs = {
        "author": import_authors,
        "category": import_categories,
        "book": import_book
    }
    if (len(sys.argv) < 2 or sys.argv[1] not in validArgs.keys()): 
        raise SyntaxError(f"No valid arguments.\nAvailable arguments: {validArgs.keys()}\nExample: python import/book/import.py author")
    
    key = sys.argv[1]
    validArgs[key]()