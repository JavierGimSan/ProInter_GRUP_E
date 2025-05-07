from rest_framework import serializers
from user.serializers import UserReadSerializer
from payment.serializers import PaymentReadSerializer
from book.serializers import BookSerializer
from .models import OrderItem, Order

class OrderItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields= "__all__"

class OrderSerializer(serializers.ModelSerializer):
    user=UserReadSerializer(read_only=True)
    orderitem_set = OrderItemSerializer(many=True, read_only=True, source='cartitem_set')
    payment=PaymentReadSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

