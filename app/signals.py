from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ingrediente, Producto
'''
@receiver(post_save, sender=Ingrediente)
def update_producto_estado(sender, instance, **kwargs):
    productos = Producto.objects.filter(
        productoingrediente__ingrediente=instance
    )

    for producto in productos:
        producto.actualizar_estado()
'''