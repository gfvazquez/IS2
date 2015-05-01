# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userstory', '0002_userstory_sprint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='activo',
            field=models.BooleanField(default=True, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userstory',
            name='comentarios',
            field=models.TextField(verbose_name=b'Comentarios', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userstory',
            name='descripcion',
            field=models.TextField(verbose_name=b'Descripcion', blank=True),
            preserve_default=True,
        ),
    ]
