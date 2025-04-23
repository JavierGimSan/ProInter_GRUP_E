from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from payment.models import Payment
from .serializers import PaymentCreateSerializer, PaymentReadSerializer

# Create your views here.

@api_view(['POST'])
def crea_payment(request):
    if request.method == 'POST':
        creaSerializer = PaymentCreateSerializer(data=request.data)
        if creaSerializer.is_valid():
            creaSerializer.save()
            return Response(creaSerializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(creaSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def info_payment(request, number):
    if request.method == "GET":
        try:
            payment = Payment.objects.get(number=number)
        except Payment.DoesNotExist:
            return Response({'error':'Esta tarjeta no está registrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer_payment = PaymentReadSerializer (payment)
        return Response(serializer_payment.data)
    
    
@api_view(['PUT', 'PATCH'])
def actualiza_info_payment(request, number):
        try:
            payment = Payment.objects.get(number=number)
        except Payment.DoesNotExist:
            return Response({'error':'Esta tarjeta no está registrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer_payment = PaymentCreateSerializer (payment, data=request.data, partial=request.method == "PATCH")
        if serializer_payment.is_valid():
            serializer_payment.save()
            return Response(serializer_payment.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_payment.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
def borrar_payment(request, number):
    if request.method == "DELETE":
        try:
            payment = Payment.objects.get(number=number)
        except Payment.DoesNotExist:
            return Response({'error':'Esta tarjeta no está registrada'}, status=status.HTTP_404_NOT_FOUND)

        payment.delete()
        #retorna que no hi ha contingut
        return Response(status=status.HTTP_204_NO_CONTENT)
