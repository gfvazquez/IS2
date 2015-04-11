from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre= models.CharField(max_length=50, verbose_name='Nombre',unique=True)
    ruc = models.CharField(max_length=20, verbose_name='Ruc',unique=True)
    numeroTelefono = models.IntegerField(max_length= 30, verbose_name='Telefono')
    representante = models.ForeignKey(User)
    estado = models.BooleanField(default = True)

    def __unicode__ (self):
        return self.nombre
