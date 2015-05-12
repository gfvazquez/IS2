# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sprint', '0005_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='duracion',
            field=models.PositiveIntegerField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sprint',
            name='fechafin',
            field=models.DateField(default=datetime.date.today),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sprint',
            name='fechainicio',
            field=models.DateField(default=datetime.date.today, blank=True),
            preserve_default=True,
        ),
    ]
