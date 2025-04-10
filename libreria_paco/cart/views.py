from rest_framework.response import Response
from .serializers import CartItemsSerializer, CartSerializer
from .models import Cart, CartItem
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status

# View para ver qué productos contiene un carrito.
@api_view(['GET'])
def ver_carrito(request, id):
    try:
        carrito = Cart.objects.get(pk=id)
    except Cart.DoesNotExist:
        return Response({'error': 'No se ha encontrado el carrito'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CartSerializer(carrito)
    return Response(serializer.data)

# View para ver un solo producto del carrito.
@api_view(['GET'])
def ver_producto(request, id):
    try:
        producto = CartItem.objects.get(pk=id)
    except CartItem.DoesNotExist:
        return Response({'error': 'No se ha encontrado el carrito'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CartItemsSerializer(producto)
    return Response(serializer.data)

@api_view(['POST'])
    