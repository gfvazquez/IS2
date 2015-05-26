# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0002_remove_actividades_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flujo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, verbose_name=b'Nombre')),
                ('descripcion', models.CharField(max_length=150)),
                ('is_active', models.BooleanField(default=True, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FlujoActividad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('orden', models.PositiveIntegerField()),
                ('actividad', models.ForeignKey(to='actividades.Actividades')),
                ('flujo', models.ForeignKey(to='flujo.Flujo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
