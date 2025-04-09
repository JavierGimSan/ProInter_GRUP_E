import requests, csv
from random import randint

AUTHOR_CSV = "import/book/author.csv"
CATEGORY_CSV = "import/book/category.csv"
BOOK_CSV = "import/book/book.csv"

def getRandomStars():
    return randint(0, 500)

def getRandomPrice():
    return randint(10, 35)

def get_book_csv(pages: int = 10):
    for page in range(1, pages):
        base_url = "https://gutendex.com"
        res = requests.get(base_url + "/books" + f"/?page={page}")

        if res.status_code != 200: return

        data = res.json()
        api_books = data.get("results")
        
        authors = []
        categories = []
        books = []

        for book in api_books:
            author_ids = append_authors(book, authors)
            category_ids = append_categories(book, categories)

            books.append([
                book.get("title", ""),
                book.get("summaries", [""])[0] if len(book.get("summaries", [""])) > 0 else "",
                "1949-06-08",
                book.get("formats", {}).get("image/jpeg", ""),
                "|".join(map(str, author_ids)),
                "|".join(map(str, category_ids)),
                getRandomPrice(),
                getRandomStars(),
                getRandomStars(),
                getRandomStars(),
                getRandomStars(),
                getRandomStars()
            ])

        author_headers = ["name"] if page == 1 else None
        book_headers = ["title","description","release","cover","author_ids","category_ids", "price","oneStarCount","twoStarCount","threeStarCount","fourStarCount","fiveStarCount"] if page == 1 else None
        save_to_csv(AUTHOR_CSV, [[name] for name in authors], author_headers)
        save_to_csv(CATEGORY_CSV, [[name] for name in categories], author_headers)
        save_to_csv(BOOK_CSV, books, book_headers)

def append_authors(book, authors):
    author_ids = []
    for author in book.get("authors"):
        if author.get("name", "") not in authors: authors.append(author.get("name", ""))
        author_ids.append(authors.index(author.get("name"))+1) 
    return author_ids if len(author_ids) > 1 else [1]

def append_categories(book, categories):
    category_ids = []
    for category_str in book.get("subjects", []):
        for category in category_str.split("--"):
            if category not in categories: categories.append(category.strip())
            category_ids.append(categories.index(category.strip())+1)
    return category_ids if len(category_ids) > 1 else [1]

def save_to_csv(filename, data, headers):
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if headers:
            writer.writerow(headers)
        writer.writerows(data)

def main():
    get_book_csv()

if __name__ == "__main__":
    main()