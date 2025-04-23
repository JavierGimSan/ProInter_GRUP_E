from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

# Create your models here.

class Payment(models.Model):
    name = models.TextField(validators=[MinLengthValidator(4)], max_length=300)
    number = models.PositiveBigIntegerField(primary_key=True)
    cvc = models.CharField(max_length=4, validators=[MinLengthValidator(3)])
    expiration = models.CharField(max_length=5,validators=[MinLengthValidator(5)])

    def clean(self):
        super().clean()
        self.valid_cvc()
        self.valid_expiration()
        self.valid_number()

    def valid_number(self):
        number_tarjeta = str(self.number)
        if len(number_tarjeta) < 12 or len(number_tarjeta) > 19:
            raise ValidationError({'PAN':'el largo del numero PAN de la tarjeta es incorrecto'})

    def valid_cvc(self):
        cvc_tarjeta = str(self.cvc)
        if len(cvc_tarjeta) < 3 or len(cvc_tarjeta) > 4:
            raise ValidationError({'cvc':'el largo del CVC es incorrecto'})        

    def valid_expiration(self):
        if len(self.expiration)==5 and self.expiration[2]=='/':
            try:
                mes, anyo = self.expiration.split('/')
                mes = int(mes)
                anyo = int(anyo)

                if mes < 1 or mes > 12:
                    raise ValidationError({'mes_expiration': 'el mes no es valido'})
                elif anyo < 24:
                    raise ValidationError({'anyo_expiration': 'la tarjeta ya esta caducada'})
            except:
                raise ValidationError({'expiration':'El formato MM/YY de la fecha de expiracion es incorrecto'})
        else:
            raise ValidationError({'expiration':'El formato MM/YY de la fecha de expiracion es incorrecto'})

def __str__(self):
    print (f"Tarjeta: ...{str(self.number)[-4:]}")