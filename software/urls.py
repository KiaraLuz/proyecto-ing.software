"""
URL configuration for software project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from app import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("roles/", views.roles, name="roles"),
    path("roles/crear/", views.rol_crear, name="rol_crear"),
    path("roles/modificar/<int:rol_id>", views.rol_modificar, name="rol_modificar"),
    path("signout/", views.signout, name="signout"),
    path("signin/", views.signin, name="signin"),
    path("usuarios/", views.usuarios, name="usuarios"),
    path("usuarios/crear/", views.usuario_crear, name="usuario_crear"),
    path("usuarios/modificar/<int:usuario_id>/", views.usuario_modificar, name="usuario_modificar"),
    path("ingredientes/", views.ingredientes, name="ingredientes"),
    path("ingredientes/crear/", views.ingrediente_crear, name="ingrediente_crear"),
    path("ingredientes/modificar/<int:ingrediente_id>", views.ingrediente_modificar, name="ingrediente_modificar"),
    path("productos/", views.productos, name="productos"),
    path("productos/crear/", views.producto_crear, name="producto_crear"),
    path("productos/modificar/<int:producto_id>", views.producto_modificar, name="producto_modificar"),
    path('recetas/', views.recetas, name='recetas'),
    path('recetas/crear/', views.receta_crear, name='receta_crear'),
    path('recetas/modificar/<int:receta_id>/', views.receta_modificar, name='receta_modificar'),
    path('costos/', views.costos, name='costos'),
    path('costos/crear/', views.costo_crear, name='costo_crear'),
    path('ganancias/', views.ganancia, name='ganancias'),
    path('ganancia/crear/', views.ganancia_crear, name='ganancia_crear'),
    path('ganancia/modificar/<int:ganancia_id>/', views.ganancia_modificar, name='ganancia_modificar'),
    path('ventas/', views.ventas, name='ventas'),
    path('venta/crear/', views.venta_crear, name='venta_crear'),
    path('obtener_precio/',views.obtener_precio, name='obtener_precio'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/crear/', views.cliente_crear, name='cliente_crear'),
    path('clientes/modificar/<int:cliente_id>/', views.cliente_modificar, name='cliente_modificar'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
