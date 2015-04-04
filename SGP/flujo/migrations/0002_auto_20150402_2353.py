# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flujo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flujo',
            name='descripcion',
            field=models.CharField(max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flujo',
            name='nombre',
            field=models.CharField(unique=True, max_length=50, verbose_name=b'Nombre'),
            preserve_default=True,
        ),
    ]
