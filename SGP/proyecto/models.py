from django.db import models
from django.contrib.auth.models import User
from flujo.models import Flujo
from cliente.models import Cliente



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
    def __unicode__(self):
        return self.usuario.username

class FlujoProyecto(models.Model):
    flujo = models.ForeignKey(Flujo)
    proyecto = models.ForeignKey(Proyecto)
    def __unicode__(self):
        return self.flujo.nombre

