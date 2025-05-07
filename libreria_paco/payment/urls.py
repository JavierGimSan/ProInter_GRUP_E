from django.urls import path, include
from payment.views import *

urlpatterns = [
    path('nuevo/', crea_payment, name='registro de tarjeta'),
    path('info/<str:number>', info_payment, name='informacion-tarjeta'),
    path('actualizar/<str:number>',actualiza_info_payment,name='actualizar-tarjeta'),
    path('borrar/<str:number>',borrar_payment, name='eliminar-tarjeta')
    # path('payment/',,name=''),

]
