__author__ = 'mauricio'
from django.db import models
from actividades.models import Actividades

ESTADOS = (

    ('Doing','Doing'),
    ('Done','Done'),
)

class Flujo(models.Model):
    nombre= models.CharField(max_length=50, verbose_name='Nombre',unique=True)
    descripcion = models.CharField(max_length = 150)
    is_active = models.BooleanField(default = True, editable=False)

    def __unicode__ (self):
        return self.nombre

#Relacion N:N entre flujos y actividades, un flujo tiene relacion con una actividad
class FlujoActividad(models.Model):
    flujo = models.ForeignKey(Flujo)
    actividad = models.ForeignKey(Actividades)
    def __unicode__(self):
        return self.flujo.nombre
