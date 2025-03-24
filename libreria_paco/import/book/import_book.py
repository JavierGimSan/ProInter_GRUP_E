import os, sys
import pandas
import django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "libreria_paco.settings")
django.setup()

from book.models import Author

AUTHOR_CSV = "import/books/author.csv"

def import_authors():
    csv = pandas.read_csv(AUTHOR_CSV)
    names = csv["name"].to_list()
    
    for name in names:
        author = Author(name=name)
        author.save()

import_authors()