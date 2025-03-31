from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator
from django.core.exceptions import ValidationError
from payment.models import Payment
from role.models import Role
# Create your models here.

class User(models.Model):
    name = models.TextField(validators=[MinLengthValidator(2)], max_length=100)
    lastName = models.TextField(validators=[MinLengthValidator(2)], max_length=150)
    email = models.TextField(validators=[MinLengthValidator(5)], max_length=320)
    password = models.TextField(validators=[MinLengthValidator(2)])
    roleId = models.ForeignKey(Role, on_delete=models.CASCADE)
    paymentId = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        super().clean()
        self.valid_email()
        

    def valid_email(self):
        validar = EmailValidator(message='Formato del correo electrónico incorrecto')
        validar(self.email)
