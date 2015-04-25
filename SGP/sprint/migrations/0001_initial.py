# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, verbose_name=b'Nombre')),
                ('estado', models.BooleanField(default=True)),
                ('fechainicio', models.DateField(default=datetime.date.today)),
                ('tiempoacumulado', models.IntegerField()),
                ('duracion', models.IntegerField()),
                ('fechafin', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
