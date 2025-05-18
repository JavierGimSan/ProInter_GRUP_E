from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import User
from cart.models import Cart

@receiver(post_save, sender=User)
def crear_carrito_usuario(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance, created_at=now().date())
