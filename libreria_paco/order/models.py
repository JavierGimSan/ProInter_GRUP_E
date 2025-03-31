from django.db import models
from django.forms import ValidationError
from book.models import Book
from user.models import User
from payment.models import Payment

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order', related_query_name='order')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='payment')

    def __str__(self):
        return f"{self.user} - {self.payment}"
    
class OrderItem(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('canceled', 'Cancelado'),
    ]
        
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='books')
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    status = models.CharField(max_length=50)

    def clean(self):
        super().clean()

        if self.quantity <= 0:
            raise ValidationError({'quantity': "Debe haber al menos un libro"})

    def __str__(self):
        return f"{self.quantity} x {self.book} - {self.status} "
