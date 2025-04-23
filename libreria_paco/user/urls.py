from django.urls import path, include
from user.views import *

urlpatterns = [
    path('registro-usuario/', crea_user, name='registro-usuario'),
    path('info-usuario/<str:pk>', info_user, name='informacion-usuario'),
    path('actualizar-usuario/<str:pk>',actualiza_user,name='actualizar-usuario'),
    path('borrar-cuenta/<str:pk>',borrar_user, name='eliminar-usuario'),
    path('todos-usuarios/', lista_usuarios, name='informacion-todos-usuario')

]