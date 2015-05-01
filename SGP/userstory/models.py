from django.db import models
from django.contrib.auth.models import User
from sprint.models import Sprint

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
PORCENTAJEREALIZADO=(
    ('0%', '0%'),
    ('10%', '10%'),
    ('20%', '20%'),
    ('30%', '30%'),
    ('40%', '40%'),
    ('50%', '50%'),
    ('60%', '60%'),
    ('70%', '70%'),
    ('80%', '80%'),
    ('90%', '90%'),
    ('100%', '100%'),
)

class Userstory(models.Model):
    nombre= models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    descripcion=models.TextField(max_length=100,blank=True,verbose_name='Descripcion')
    tiempoestimado=models.IntegerField(default=0, verbose_name='Tiempo Estimado')#endias
    tiempotrabajado=models.IntegerField(default=0, verbose_name='Tiempo Trabajado') #enhoras
    #adjuntoasociado=models.FileField()
    comentarios= models.TextField(max_length=100,blank=True,verbose_name='Comentarios')
    usuarioasignado=models.ForeignKey(User, verbose_name='Asignado a: ')
    estado=models.CharField(max_length=10, choices=ESTADOS, default="Nueva",verbose_name='Estado:')
    prioridad=models.CharField(max_length=10,default = True, choices=PRIORIDAD, verbose_name= 'Prioridad: ')
    porcentajerealizado=models.CharField(max_length=10, choices=PORCENTAJEREALIZADO, default="<0%>", verbose_name= 'Porcentaje Realizado: ')
    historial=models.CharField(max_length=1000,blank=True, editable=False,verbose_name='Historico')# poner en otro lado, no es algo que el usuario crea
    activo = models.BooleanField(default=True, editable=False) #para la eliminacion
    sprint = models.ForeignKey(Sprint)

    def __unicode__ (self):
        return self.nombre
