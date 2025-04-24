from django.shortcuts import render
from requests import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import OrderSerializer, OrderItemSerializer
from user.models import User
from  .models import Order, OrderItem

#View para ver los productos que contiene una orden 
@api_view(["GET"])
def ver_orden(request, id):
    try:
        orden = Order.objects.get(pk=id)
    except Order.DoesNotExist:
        return Response(
            {"error": "No se ha encontrado la orden"},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    serializer = OrderSerializer(orden)
    return Response(serializer.data)

#View para ver todas las órdenes de un usuario
@api_view(["GET"])
def ver_ordenes(request, id):
    try: 
        user = User.objects.get(pk=id)
    except:
        return Response(
            {"error": "No se ha encontrado el usuario"}
        )
    orders = Order.objects.filter(user=user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#View para ver un Order Item
@api_view(['GET'])
def ver_producto(request, id):
    try:
        producto = OrderItem.objects.get(pk=id)
    except OrderItem.DoesNotExist:
        return Response(
            {"error": "No se ha encontrado el producto"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = OrderItemSerializer(producto)
    return Response(serializer.data)

#View para crear una orden
@api_view(['POST'])
def crear_orden(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#View para añadir un orderItem a la orden
@api_view(["POST"])
def agregar_producto(request):
    serializer = OrderItemSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#View para borrar una orden completa
@api_view(["DELETE"])
def borrar_orden(request, id):
    try:
        order = Order.objects.get(pk=id)
    except Order.DoesNotExist:
        return Response(
            {"error": "No se ha encontrado la orden"},
            status = status.HTTP_404_NOT_FOUND,
        )
    order.delete()
    return Response({"message": "Orden eliminada con éxito"})

#View para eliminar un order item de la orden
@api_view(["DELETE"])
def borrar_producto(request, id):
    try:
        orderItem = OrderItem.objects.get(pk=id)
    except OrderItem.DoesNotExist:
        return Response(
            {"error": "Producto no encontrado"},
            status=status.HTTP_404_NOT_FOUND,
        )
    orderItem.delete()
    return Response({"message": "Producto eliminado con éxito"})

#View para actualizar un order item
@api_view(["PATCH"])
def actualizar_producto(request, id):
    try:
        orderItem = OrderItem.objects.get(pk=id)
    except OrderItem.DoesNotExist:
        return Response(
            {"error": "El producto no existe"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.data.get("quantity"):
        orderItem.quantity=request.data.get("quantity")
      
    if request.data.get("status"):
        status_value=request.data.get("status")
        if status_value in dict(OrderItem.STATUS_CHOICES):
            orderItem.status = status_value
        else:
            return Response(
                {"error": "El estado no es válido"},
                status= status.HTTP_400_BAD_REQUEST,
            )
    orderItem.save()    
    return Response(
        {"message": "Producto actualizado"},
        status=status.HTTP_200_OK,
    )
