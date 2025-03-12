from django.db import models

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    created_at = models.DateField()

    def __str__(self):
        return f"{self.user} - {self.created_at}"

class CartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart')
    quantity = models.IntegerField()

    def __str__(self):
       return f"{self.book} x {self.quantity}"
