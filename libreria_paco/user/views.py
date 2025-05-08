from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from .serializers import UserCreateSerializer, UserReadSerializer, UserReadAllSerializer
# Create your views here.

@api_view(['POST'])
def crea_user(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def lista_usuarios(request):
    if request.method == 'GET':
        todos_user = User.objects.all()
        listaSerializer = UserReadAllSerializer(todos_user, many=True)
        return Response(listaSerializer.data)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def info_user(request, pk):
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error':'Este usuario no está registrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserReadSerializer(user)
        return Response(serializer.data)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT', 'PATCH'])
def actualiza_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error':'Este usuario no está registrado'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserCreateSerializer(user, data=request.data, partial=request.method == "PATCH")
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def borrar_user(request, pk):
    if request.method == "DELETE":
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error':'Este usuario no está registrado'}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
