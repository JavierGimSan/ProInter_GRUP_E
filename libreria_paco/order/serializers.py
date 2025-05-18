from rest_framework import serializers
from user.serializers import UserReadSerializer
from payment.serializers import PaymentReadSerializer
from book.serializers import BookSerializer
from .models import OrderItem, Order
from user.models import User
from payment.models import Payment

class OrderItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields= "__all__"

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    orderitem_set = OrderItemSerializer(many=True, read_only=True, source='cartitem_set')
    payment = serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all())

    class Meta:
        model = Order
        fields = "__all__"

