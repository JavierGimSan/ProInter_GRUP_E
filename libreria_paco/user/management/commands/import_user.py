import csv
import os
from user.models import User
from role.models import Role
from payment.models import Payment
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):

    def handle(self, *args, **options):
        directorio = os.path.join(settings.BASE_DIR, 'import', 'user', 'users.csv')
        #uso esto para llamar a la ruta absoluta

        with open(directorio, encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                try:
                    email = row['email'].replace(' ','').lower()

                    if User.objects.filter(email=email).exists():
                        print(f"El correo {row['email']} ya está registrado")
                        continue 
                    #con el continue, salta a la siguiente fila del csv, asi evito que
                    #se registre un email dos veces, como suelen hacer en las webs
                    
                    try:
                        role = Role.objects.get(name=row['roleId'].strip())
                    except Role.DoesNotExist:
                        print(f"El rol {row['roleId']} no existe")
                        continue

                    payment = None
                    if row.get("paymentId"):
                        try:
                            payment = Payment.objects.get(pk=int(row['paymentId'].replace(' ','')))
                        except (Payment.DoesNotExist,ValueError):
                            payment_row = row['paymentId'].replace(' ','')
                            if len(payment_row)>4:
                                last_4 = payment_row[-4:]
                            else:
                                last_4 = payment_row

                            print(f"La tarjeta ...{last_4} no está registrada. No se creará el usuario")
                            continue

                    user = User(
                        name = row['name'].strip(),
                        lastName = row['lastName'].strip(),
                        email = email,
                        password = row['password'].strip(),
                        roleId = role,
                        paymentId = payment
                    )
                    #Con el full clean llamo a todas las validaciones, 
                    #como MinLengthValue o el clean(self) que creé en models
                    user.full_clean()
                    user.save()
                    print(f"Usuario {row['name']} {row['lastName']} añadido")

                except Exception as e:
                    print(f"Usuario {row['name']} {row['lastName']} no añadido: {str(e)}")
