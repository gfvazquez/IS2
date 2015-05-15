from django.db import models
from django.contrib.auth.models import User
from flujo.models import Flujo, FlujoActividad
from cliente.models import Cliente
from sprint.models import Sprint
from userstory.models import Userstory
from django.contrib.auth.models import Group, Permission, User
from actividades.models import Actividades


ESTADOS = (

        ('ToDo','ToDo'),
        ('Doing','Doing'),
        ('Done','Done'),
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

    def __unicode__ (self):
        return self.nombre

    #class Meta:
    #    ordering = ["nombre"]
    #    permissions = (
    #                      ("listar_miembros", "Puede listar los miembros de un proyecto"),
    #                      ("importar_proyectos", "Puede importar proyectos"),
    #                      ("consultar_proyectos", "Puede consultar proyectos"),
    #                      ("consultar_proyectosfinalizados", "Puede consultar proyectos finalizados"),
    #                  )

class Equipo(models.Model):
    usuario = models.ForeignKey(User)
    proyecto = models.ForeignKey(Proyecto)
    rol = models.ForeignKey(Group)
    def __unicode__(self):
        return self.usuario.username

class FlujoProyecto(models.Model):
    flujo = models.ForeignKey(Flujo)
    proyecto = models.ForeignKey(Proyecto)
    sprint = models.ForeignKey(Sprint, default=1)
    estado = models.CharField(max_length=15, default='Inactivo')
    def __unicode__(self):
        return self.flujo.nombre

class ProyectoFlujoActividad(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    flujoActividad = models.ForeignKey(FlujoActividad)
    userStory = models.ForeignKey(Userstory)
    estadoActividad = models.CharField(max_length=5, choices=ESTADOS, editable=False, blank=True) #blank true para queguarde como vacio en la bd al crear
    def __unicode__(self):
        return self.proyecto.nombre

