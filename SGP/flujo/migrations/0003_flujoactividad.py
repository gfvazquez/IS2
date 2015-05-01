# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0001_initial'),
        ('flujo', '0002_auto_20150402_2353'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlujoActividad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actividad', models.ForeignKey(to='actividades.Actividades')),
                ('flujo', models.ForeignKey(to='flujo.Flujo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
