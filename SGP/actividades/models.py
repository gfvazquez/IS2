from django.db import models

ESTADOS = (

    ('ToDo','ToDo'),
    ('Doing','Doing'),
    ('Done','Done'),
)

class Actividades(models.Model):
    nombre= models.CharField(max_length=50, verbose_name='Nombre:', unique=True)
    #orden debe estar dentro de la relacion muchos a muchos
    estado = models.CharField(max_length=5, choices=ESTADOS, editable=False, blank=True) #blank true para queguarde como vacio en la bd al crear
    is_active = models.BooleanField(default=True, editable=False)

    def __unicode__ (self):
        return self.nombre

