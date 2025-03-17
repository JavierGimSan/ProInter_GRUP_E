from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
# Create your models here.

class Role(models.Model):
    name = models.TextField(validators=[MinLengthValidator(2)], max_length=150)