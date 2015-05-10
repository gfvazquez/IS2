# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sprint', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='duracion',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sprint',
            name='estado',
            field=models.TextField(default=b'Creado', max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sprint',
            name='fechafin',
            field=models.DateField(default=datetime.date(2015, 5, 10)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sprint',
            name='tiempoacumulado',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
    ]
