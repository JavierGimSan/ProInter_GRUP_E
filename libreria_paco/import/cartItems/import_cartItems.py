import django
import pandas as pd
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "libreria_paco.settings")
django.setup()


from cart.models import CartItem

def importar_csv_cartItems():
    df = pd.read_csv("./import/cartItems/cartItems.csv")
    # print(df.head())
    cartItems = [
        CartItem(
            id = row["id"],
            book_id = row["book_id"],
            cart_id = row["cart_id"],
            quantity = row["quantity"]
        )
        for _, row in df.iterrows()
    ]

    CartItem.objects.bulk_create(cartItems)
    print("CartItems importados con éxito!")

importar_csv_cartItems()
