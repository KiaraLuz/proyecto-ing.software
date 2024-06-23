from django.db import models

# Create your models here.
class Rol(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    nombre_rol = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField(default=True)
class Usuario(models.Model):
    id_usuario=models.CharField(max_length=15, primary_key=True)
    nombre_usuario = models.CharField(max_length=50)
    rol_usuario = models.ForeignKey(Rol, on_delete=models.CASCADE)
