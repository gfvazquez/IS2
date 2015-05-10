__author__ = 'mauricio'
from django.db import models
import datetime


ESTADOS = (
    ('CREADO','Creado'),
    ('INI','Iniciado'),
    ('FIN','Finalizado'),
)

class Sprint(models.Model):
  nombre= models.CharField(max_length=50, verbose_name='Nombre', unique=True)
  estado=models.TextField(max_length=10, default="Creado")
  activo = models.BooleanField(default = True)
  fechainicio=models.DateField(default=datetime.date.today)
  tiempoacumulado=models.IntegerField(default=0,blank=True)
  fechafin=models.DateField(default= datetime.date.today())
  duracion=models.IntegerField(default=0)

  def __unicode__ (self):
      return self.nombre

