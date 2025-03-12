from django.db import models

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
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

    def __str__(self):
        return f"{self.quantity} x {self.book} - {self.status} "
