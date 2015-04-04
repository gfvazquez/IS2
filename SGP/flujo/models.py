__author__ = 'mauricio'
from django.db import models

class Flujo(models.Model):
    nombre= models.CharField(max_length=50, verbose_name='Nombre',unique=True)
    descripcion = models.CharField(max_length = 150)
    estado = models.BooleanField(default = True)