from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ingrediente, RecetaIngrediente, CostoProducto, Producto

@receiver(post_save, sender=Ingrediente)
def update_cost_product(sender, instance, **kwargs):
    recetas = RecetaIngrediente.objects.filter(ingrediente=instance)
    
    for receta in recetas:
        producto = receta.receta.producto

        try:
            costo_producto = CostoProducto.objects.get(producto=producto)
        except CostoProducto.DoesNotExist:
            continue
        
        costo_producto.calcular_costo_total()

'''
@receiver(post_save, sender=Ingrediente)
def update_producto_estado(sender, instance, **kwargs):
    productos = Producto.objects.filter(
        productoingrediente__ingrediente=instance
    )

    for producto in productos:
        producto.actualizar_estado()
'''