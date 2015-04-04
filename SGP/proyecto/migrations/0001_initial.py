# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('auto_increment_id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=30)),
                ('estado', models.CharField(default=b'Iniciado', max_length=15, choices=[(b'Iniciado', b'Iniciado'), (b'Finalizado', b'Finalizado'), (b'Cancelado', b'Cancelado')])),
                ('fecha_inicio', models.DateField()),
                ('duracion_estimada', models.IntegerField()),
                ('descripcion', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['nombre'],
                'permissions': (('listar_miembros', 'Puede listar los miembros de un proyecto'), ('importar_proyectos', 'Puede importar proyectos'), ('consultar_proyectos', 'Puede consultar proyectos'), ('consultar_proyectosfinalizados', 'Puede consultar proyectos finalizados')),
            },
            bases=(models.Model,),
        ),
    ]
