"""libreria_paco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from cart.views import actualizar_producto, agregar_producto, borrar_carrito, borrar_producto, crear_carrito, ver_carrito, ver_carrito, ver_producto
from order.views import borrar_orden, crear_orden, ver_orden, ver_ordenes

urlpatterns = [
    path("admin/", admin.site.urls),
    path("carrito/<int:id>", ver_carrito, name="ver_carrito"),
    path("carrito/borrar/<int:id>/", borrar_carrito, name="borrar_carrito"),
    path("carrito/crear/", crear_carrito, name="crear_carrito"),
    path("carrito/usuario/<int:id>/", ver_carrito, name="ver_carrito_usuario"),
    path("producto/<int:id>", ver_producto, name="ver_producto"),
    path("producto/borrar/<int:id>/", borrar_producto, name="borrar_producto"),
    path("producto/agregar/", agregar_producto, name="agregar_producto"),
    path("producto/actualizar/<int:id>/", actualizar_producto, name="actualizar_producto"),
    path("orden/<int:id>/", ver_orden, name="ver_orden"),
    path("orden/usuario/<int:id>/", ver_ordenes, name="ver_ordenes_usuario"),
    path("orden/crear/", crear_orden, name="crear_orden"),
    path("orden/borrar/<int:id>/", borrar_orden, name="borrar_orden"),
    path('payment/', include('payment.urls')),
    path('user/', include('user.urls')),
    path('', include('book.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
