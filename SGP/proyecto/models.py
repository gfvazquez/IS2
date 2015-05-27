from django.db import models
import datetime
from flujo.models import Flujo, FlujoActividad
from cliente.models import Cliente
from django.contrib.auth.models import Group, Permission, User
from actividades.models import Actividades


ESTADOS = (

        ('ToDo','ToDo'),
        ('Doing','Doing'),
        ('Done','Done'),
    )


ESTADOS_User_Story = (

    ('Nueva','Nueva'),
    ('InPlanning','InPlanning'),
    ('EnCurso','EnCurso'),
    ('Resuelta','Resuelta'),
    ('Comentario','Comentario'),
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

class Proyecto(models.Model):

    ESTADOS_PROYECTO=(
        ('Iniciado', 'Iniciado'),
        ('Finalizado', 'Finalizado'),
        ('Cancelado', 'Cancelado'),
    )

    auto_increment_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    #lider = models.ForeignKey(User, null=True)
    estado = models.CharField(max_length=15, choices=ESTADOS_PROYECTO, default='Iniciado')
    fecha_inicio = models.DateField()
    duracion_estimada = models.IntegerField()
    descripcion = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    usuarios_proyecto = models.ManyToManyField(User, through='Equipo')
    cliente = models.ForeignKey(Cliente)

    #flujo

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        permissions = (
                          ("asignar_equipo", "Puede asignar un usuario al proyecto"),
                          ("asignar_flujo", "Puede asignar un flujo al proyecto"),
                          ("asignar_sprint", "Puede asignar un Sprint a un Flujo-Proyecto"),
                          ("reasignar_sprint", "puede reasignar un Sprint a un Flujo-Proyecto"),
                      )

class Equipo(models.Model):
    usuario = models.ForeignKey(User)
    proyecto = models.ForeignKey(Proyecto)
    rol = models.ForeignKey(Group)
    def __unicode__(self):
        return self.usuario.username


'''ESTADOS = (
    ('CREADO','Creado'),
    ('INI','Iniciado'),
    ('FIN','Finalizado'),
)'''

class Sprint(models.Model):
    nombre= models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    estado=models.TextField(max_length=10, default="Creado")
    activo = models.BooleanField(default = True)
    fechainicio=models.DateField(null=True,blank=True,default=datetime.date.today)
    tiempoacumulado=models.IntegerField(blank=True,default=0)
    fechafin=models.DateField(default= datetime.date.today)
    duracion=models.PositiveIntegerField(blank=True,default=0)
    proyecto = models.ForeignKey(Proyecto)


    def save(self):
        from datetime import datetime, timedelta
        d = timedelta(days=self.duracion)
        if self.fechainicio:
         self.fechafin = self.fechainicio + d
         super(Sprint, self).save()
        else:
         self.fechafin = self.fechafin
         super(Sprint, self).save()

    def __unicode__(self):
        return self.nombre

class FlujoProyecto(models.Model):
    flujo = models.ForeignKey(Flujo)
    proyecto = models.ForeignKey(Proyecto)
    sprint = models.ForeignKey(Sprint, default=1)
    estado = models.CharField(max_length=15, default='Inactivo')
    def __unicode__(self):
        return self.flujo.nombre



class Userstory(models.Model):
    nombre= models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    descripcion=models.TextField(max_length=100,blank=True,verbose_name='Descripcion')
    tiempoestimado=models.IntegerField(default=0, verbose_name='Tiempo Estimado')#endias
    tiempotrabajado=models.IntegerField(default=0, verbose_name='Tiempo Trabajado',null=True,blank=True) #enhoras
    #adjuntoasociado=models.FileField()
    comentarios= models.TextField(max_length=100,blank=True,verbose_name='Comentarios')
    usuarioasignado=models.ForeignKey(User, verbose_name='Asignado a: ')
    estado=models.CharField(max_length=10, choices=ESTADOS_User_Story, default="Nueva",verbose_name='Estado:')
    prioridad=models.CharField(max_length=10,default = True, choices=PRIORIDAD, verbose_name= 'Prioridad: ')
    porcentajerealizado=models.CharField(max_length=10, choices=PORCENTAJEREALIZADO, default="<0%>", verbose_name= 'Porcentaje Realizado: ')
    historial=models.CharField(max_length=1000,blank=True, editable=False,verbose_name='Historico')# poner en otro lado, no es algo que el usuario crea
    activo = models.BooleanField(default=True, editable=False) #para la eliminacion
    sprint = models.ForeignKey(Sprint)

    def __unicode__(self):
        return self.nombre


class ProyectoFlujoActividad(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    flujoActividad = models.ForeignKey(FlujoActividad)
    userstory = models.ForeignKey(Userstory)
    estado = models.CharField(max_length=5, choices=ESTADOS, editable=False, blank=True) #blank true para queguarde como vacio en la bd al crear

    def __unicode__(self):
        return self.proyecto.nombre

