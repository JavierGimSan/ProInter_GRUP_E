from rest_framework import serializers
from .models import CartItem, Cart


class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['book', 'cart', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'created_at', 'items']
