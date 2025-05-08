from django.urls import path
from user.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('registro-usuario/', crea_user, name='registro-usuario'),
    path('info-usuario/<str:pk>', info_user, name='informacion-usuario'),
    path('actualizar-usuario/<str:pk>',actualiza_user,name='actualizar-usuario'),
    path('borrar-cuenta/<str:pk>',borrar_user, name='eliminar-usuario'),
    path('todos-usuarios/', lista_usuarios, name='informacion-todos-usuario')

]