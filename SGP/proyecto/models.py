from django.db import models
from django.contrib.auth.models import User

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
    descripcion = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    usuarios_proyecto = models.ManyToManyField(User, through='Equipo')
    #flujo

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
        return '%s | %s' % (self.usuario, self.proyecto)
