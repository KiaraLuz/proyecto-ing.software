from django.db import models

# Create your models here.
class Rol(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    nombre_rol = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_rol

class Usuario(models.Model):
    id_usuario=models.CharField(max_length=15, primary_key=True)
    nombre_usuario = models.CharField(max_length=50)
    rol_usuario = models.ForeignKey(Rol, on_delete=models.CASCADE)
    contraseña_usuario = models.CharField(max_length=20) 
class Ingrediente(models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    nombre_ingrediente = models.CharField(max_length=100)  
    cantidad = models.DecimalField(max_digits=10, decimal_places=2) 
    unidad = models.CharField(max_length=10)
    estado_ingrediente = models.CharField(max_length=20)