import csv
import os
from django.core.management.base import BaseCommand
from role.models import Role
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        directorio = os.path.join(settings.BASE_DIR, 'import', 'role', 'roles.csv')
        #uso esto para llamar a la ruta absoluta

        with open(directorio, encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                try:
                    name = row['name'].strip()

                    if Role.objects.filter(name=name).exists():
                        print(f"Rol {row['name']} ya existe")
                        continue

                    rol = Role(
                        name = name
                    )
                    #Con el full clean llamo a todas las validaciones, 
                    #como MinLengthValue o el clean(self) que creé en models
                    rol.full_clean()

                    rol.save()
                    print(f"Rol {row['name']} añadido")

                except Exception as e:
                    print(f"Rol {row['name']} no añadido: {str(e)}")
