__author__ = 'mauricio'
import datetime
from datetime import timedelta
from django.db import models

ESTADOS = (
    ('CREADO','Creado'),
    ('INI','Iniciado'),
    ('FIN','Finalizado'),
)

class Sprint(models.Model):
    nombre= models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    estado=models.TextField(max_length=10, default="Creado")
    activo = models.BooleanField(default = True)
    fechainicio=models.DateField(null=True,blank=True,default=datetime.date.today)
    tiempoacumulado=models.IntegerField(blank=True,default=0)
    fechafin=models.DateField(default= datetime.date.today)
    duracion=models.PositiveIntegerField(blank=True,default=0)

    def save(self):
        from datetime import datetime, timedelta
        d = timedelta(days=self.duracion)
        if self.fechainicio:
         self.fechafin = self.fechainicio + d
         super(Sprint, self).save()
        else:
         self.fechafin = self.fechafin
         super(Sprint, self).save()



    def __unicode__ (self):
        return self.nombre