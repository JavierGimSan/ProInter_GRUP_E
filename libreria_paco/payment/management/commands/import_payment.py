import csv
import os
from payment.models import Payment
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):

    def handle(self, *args, **options):

# def import_payment():
        directorio = os.path.join(settings.BASE_DIR, 'import', 'payment', 'payments.csv')
        #uso esto para llamar a la ruta absoluta

        with open(directorio, encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                try:
                    number = row['number'].replace(' ','')
                    last_4 = number[-4:]

                    pago = Payment(
                        name = row['name'].strip(),
                        number = number,
                        cvc = row['cvc'].replace(' ',''),
                        expiration = row['expiration'].replace(' ','')
                    )
                    #Con el full clean llamo a todas las validaciones, 
                    #como MinLengthValue o el clean(self) que creé en models
                    pago.full_clean()
                    pago.save()

                    print(f"tarjeta ...{last_4} añadida")

                except Exception as e:
                    print(f"Tarjeta no añadida: {str(e)}")
