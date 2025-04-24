from rest_framework import serializers
from .models import Cart, CartItem
from user.serializers import UserSerializer
from book.serializers import BookSerializer

class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    cart = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = CartItem
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    cartitem_set = CartItemSerializer(many=True, read_only=True, source='cartitem_set')

    class Meta:
        model = Cart
        fields = "__all__"


