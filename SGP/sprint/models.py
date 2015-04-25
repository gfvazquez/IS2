__author__ = 'mauricio'
import datetime
from datetime import timedelta
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
    fechafin=models.DateField(default= datetime.date.today())
    duracion=models.PositiveIntegerField(default=0)
    #userstory=models.ManyToOneRel(Userstory)

    def __unicode__ (self):
        return self.nombre

