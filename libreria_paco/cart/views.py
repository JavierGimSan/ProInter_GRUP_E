from rest_framework.response import Response
from .serializers import CartItemSerializer, CartSerializer
from .models import Cart, CartItem
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from user.models import User


# View para ver los productos que contiene un carrito.
@api_view(["GET"])
def ver_carrito(request, id):
    try:
        carrito = Cart.objects.get(pk=id)
    except Cart.DoesNotExist:
        return Response(
            {"error": "No se ha encontrado el carrito"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = CartSerializer(carrito)
    return Response(serializer.data)


# View para ver los carritos pertenecientes a un usuario
@api_view(["GET"])
def ver_carritos(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response(
            {"error": "No se ha encontrado el usuario"},
            status=status.HTTP_404_NOT_FOUND,
        )
    carts = Cart.objects.filter(user=user)
    serializer = CartSerializer(carts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# View para ver un solo producto del carrito.
@api_view(["GET"])
def ver_producto(request, id):
    try:
        producto = CartItem.objects.get(pk=id)
    except CartItem.DoesNotExist:
        return Response(
            {"error": "No se ha encontrado el producto"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = CartItemSerializer(producto)
    return Response(serializer.data)

#View para crear un nuevo carrito
@api_view(["POST"])
def crear_carrito(request):
    serializer = CartSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#View para crear un nuevo cartItem
@api_view(["POST"])
def agregar_producto(request):
    serializer = CartItemSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#View para borrar un carrito entero
@api_view(["DELETE"])
def borrar_carrito(request, id):
    try:
        cart = Cart.objects.get(pk=id)
    except Cart.DoesNotExist:
        return Response(
            {"error": "No se ha encontrado el carrito"},
            status=status.HTTP_404_NOT_FOUND,
        )
    cart.delete()
    return Response({"message": "Carrito eliminado con éxito"})

#View para borrar un cartItem dentro del carrito.
@api_view(["DELETE"])
def borrar_producto(request, id):
    try:
        cartItem = CartItem.objects.get(pk=id)
    except CartItem.DoesNotExist:
        return Response(
            {"error": "No se ha encontrado el producto"},
            status=status.HTTP_404_NOT_FOUND,
        )
    cartItem.delete()
    return Response({"message": "Producto eliminado con éxito"})

#View para actualizar la cantidad de un cratItem
@api_view(['PATCH'])
def actiualizar_producto(request, id):
    try:
        cartItem = CartItem.objects.get(pk=id)
    except CartItem.DoesNotExist:
        return Response(
            {"error": "No se ha encontrado el producto"},
            status=status.HTTP_404_NOT_FOUND,
        )
    if request.data.get("quantity"):
        cartItem.quantity=request.data.get("quantity")
        cartItem.save()
        return Response(
            {"message": "Producto actualizado"},
            status=status.HTTP_200_OK,
        )
    return Response(
        {"error": "Cantidad no indicada"},
        status=status.HTTP_404_NOT_FOUND,
    )