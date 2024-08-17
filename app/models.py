from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

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

class UnidadesMedida(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Ingrediente(models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    nombre_ingrediente = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=10)
    precio_ingrediente = models.DecimalField(max_digits=10, decimal_places=2)
    estado_ingrediente = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_ingrediente
    
    def clean(self):
        if self.precio_ingrediente < 0:
            raise ValidationError('El precio del ingrediente no puede ser negativo.')

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    
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

class CostoProducto(models.Model):
    id_costo = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ingredientes = models.ManyToManyField(Ingrediente, through='CostoProductoIngrediente')
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Costo de {self.producto.nombre_producto} - {self.costo_total if self.costo_total else 'No calculado'}"

    def calcular_costo_total(self):
        receta_ingredientes = RecetaIngrediente.objects.filter(receta__producto=self.producto)
        costo_total = sum(ri.cantidad * ri.ingrediente.precio_ingrediente for ri in receta_ingredientes)
        self.costo_total = costo_total
        self.save()

class CostoProductoIngrediente(models.Model):
    costo_producto = models.ForeignKey(CostoProducto, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_ingrediente = models.DecimalField(max_digits=10, decimal_places=2)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.ForeignKey(UnidadesMedida, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.costo_producto.producto.nombre_producto} - {self.ingrediente.nombre_ingrediente}: {self.costo_total}"
    
class Ganancia(models.Model):
    id_ganancia = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    costo_producto = models.DecimalField(max_digits=10, decimal_places=2)
    precio_con_ganancia = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Ganancia para {self.nombre_producto}'

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=100)
    correo_cliente = models.EmailField(blank=True, null=True)
    telefono_cliente = models.CharField(max_length=9,blank=True, null=True)
    def __str__(self):
        return self.nombre_cliente
    
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    fecha = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        try:
            ganancia = Ganancia.objects.get(nombre_producto=self.producto.nombre_producto)
            self.precio = ganancia.precio_con_ganancia
        except Ganancia.DoesNotExist:
            self.precio = 0
        super().save(*args, **kwargs)