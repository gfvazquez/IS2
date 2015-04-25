# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Userstory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, verbose_name=b'Nombre')),
                ('descripcion', models.TextField(verbose_name=b'Descripcion')),
                ('tiempoestimado', models.IntegerField(default=0, verbose_name=b'Tiempo Estimado')),
                ('tiempotrabajado', models.IntegerField(default=0, verbose_name=b'Tiempo Trabajado')),
                ('comentarios', models.TextField(verbose_name=b'Comentarios')),
                ('estado', models.CharField(default=b'<no asignado>', max_length=10, verbose_name=b'Estado:', choices=[(b'Nueva', b'Nueva'), (b'InPlanning', b'InPlanning'), (b'EnCurso', b'EnCurso'), (b'Resuelta', b'Resuelta'), (b'Comentarios', b'Comentarios'), (b'Validado', b'Validado'), (b'Cancelado', b'Cancelado')])),
                ('prioridad', models.CharField(default=True, max_length=10, verbose_name=b'Prioridad: ', choices=[(b'Normal', b'Normal'), (b'Baja', b'Baja'), (b'Alta', b'Alta')])),
                ('porcentajerealizado', models.CharField(default=b'<0%>', max_length=10, verbose_name=b'Porcentaje Realizado: ', choices=[(b'0%', b'0%'), (b'10%', b'10%'), (b'20%', b'20%'), (b'30%', b'30%'), (b'40%', b'40%'), (b'50%', b'50%'), (b'60%', b'60%'), (b'70%', b'70%'), (b'80%', b'80%'), (b'90%', b'90%'), (b'100%', b'100%')])),
                ('activo', models.BooleanField(default=True)),
                ('usuarioasignado', models.ForeignKey(verbose_name=b'Asignado a: ', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
