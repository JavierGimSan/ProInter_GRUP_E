import django
import pandas as pd
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "libreria_paco.settings")
django.setup()


from cart.models import Cart

def importar_csv_cart():
    df = pd.read_csv("./import/cart/cart.csv")
    # print(df.head())
    carts = [
        Cart(
            id = row["id"],
            user_id = row["userId"],
            created_at = row["created_at"]
        )
        for _, row in df.iterrows()
    ]

    Cart.objects.bulk_create(carts)
    print("Carts importados con éxito!")

importar_csv_cart()
