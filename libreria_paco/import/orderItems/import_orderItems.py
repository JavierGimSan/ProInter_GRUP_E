import django
import pandas as pd
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "libreria_paco.settings")  # Asegúrate de usar el nombre correcto de tu proyecto
django.setup()


from order.models import OrderItem

def importar_csv_order():
    df = pd.read_csv("./import/orderItems/orderItems.csv")
    # print(df.head())
    orderItems = [
        OrderItem(
            id = row["id"],
            book_id = row["book_id"],
            quantity = row["quantity"],
            order_id=row["order_id"],
            status=["status"]
        )
        for _, row in df.iterrows()
    ]

    OrderItem.objects.bulk_create(orderItems)
    print("OrderItems importados con éxito!")

importar_csv_order()
