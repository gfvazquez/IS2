__author__ = 'mauricio'
import datetime
from django.db import models

ESTADOS = (

    ('INI','Iniciado'),
    ('FIN','Finalizado'),
)

class Sprint(models.Model):
    nombre= models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    estado=models.TextField(max_length=10, default="Iniciado")
    activo = models.BooleanField(default = True)
    fechainicio=models.DateField(default=datetime.date.today)
    tiempoacumulado=models.IntegerField()
    duracion=models.IntegerField()
    fechafin=models.DateField()

    def __unicode__ (self):
        return self.nombre

