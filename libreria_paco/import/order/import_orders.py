import django
import pandas as pd
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "libreria_paco.settings")  # Asegúrate de usar el nombre correcto de tu proyecto
django.setup()


from order.models import Order

def importar_csv_order():
    df = pd.read_csv("./import/order/orders.csv")
    # print(df.head())
    orders = [
        Order(
            id = row["id"],
            user_id = row["userId"],
            payment_id = row["payment"]
        )
        for _, row in df.iterrows()
    ]

    Order.objects.bulk_create(orders)
    print("Orders importadas con éxito!")

importar_csv_order()
