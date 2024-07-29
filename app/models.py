from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_rol


class Usuario(AbstractUser):
    id = models.AutoField(primary_key=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return self.username

    @property
    def is_rol_admin(self):
        return self.rol.is_admin if self.rol else False


class Ingrediente(models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    nombre_ingrediente = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=10)
    estado_ingrediente = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_ingrediente


class UnidadesMedida(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

from django.db import models

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    #ingredientes = models.ManyToManyField('Ingrediente', through='ProductoIngrediente')
   # estado_producto = models.BooleanField(default=True)

   # def actualizar_estado(self):
       # if self.ingredientes.filter(estado_ingrediente=False).exists():
           # self.estado_producto = False
        #else:
           # self.estado_producto = True
        #self.save()

    def __str__(self):
        return self.nombre_producto

class Receta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ingredientes = models.ManyToManyField(Ingrediente, through='RecetaIngrediente')

class RecetaIngrediente(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.ForeignKey(UnidadesMedida, on_delete=models.CASCADE)
'''
class ProductoIngrediente(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
'''   
class PrecioProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE,default=1)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre_producto} - {self.precio_producto}"

class PrecioIngrediente(models.Model):
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    precio_ingrediente = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.ForeignKey(UnidadesMedida, on_delete=models.CASCADE,default=1)  

    def __str__(self):
        return f"{self.ingrediente.nombre_ingrediente} - {self.precio_ingrediente} ({self.unidad.nombre})"
    
