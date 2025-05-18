from rest_framework import serializers
from .models import Cart, CartItem
from book.serializers import BookSerializer

class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    cart = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = CartItem
        fields = "__all__"

class CreateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart', 'book', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"


