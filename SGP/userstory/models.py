__author__ = 'mauricio'
import datetime
from django.db import models

ESTADOS = (

    ('Nueva','Nueva'),
    ('InPlanning','InPlanning'),
    ('EnCurso','EnCurso'),
    ('Resuelta','Resuelta'),
    ('Comentarios','Comentarios'),
    ('Validado','Validado'),
    ('Cancelado','Cancelado'),
)
PRIORIDAD=(
    ('Normal', 'Normal'),
    ('Baja', 'Baja'),
    ('Alta', 'Alta'),
)

class Userstory(models.Model):
    nombre= models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    descripcion=models.TextField()
    tiempoestimado=models.IntegerField(default=0)
    tiempotrabajado=models.IntegerField(default=0)
    #adjuntoasociado=models.FileField()
    #usuarioasignado=models.CharField()
    #flujoasociado=models.CharField()
    #sprintasociado=models.CharField()
    estado=models.CharField(max_length=10, choices=ESTADOS, default="<no asignado>")
    prioridad=models.CharField(default = True, choices=PRIORIDAD)
    porcentajerealizado=models.IntegerField(default=0)
    historial=models.TextField()
    activo = models.BooleanField()

    def __unicode__ (self):
        return self.nombre

