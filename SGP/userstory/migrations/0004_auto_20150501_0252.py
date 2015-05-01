# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userstory', '0003_auto_20150501_0246'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstory',
            name='historial',
            field=models.CharField(max_length=1000, verbose_name=b'Historico', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userstory',
            name='comentarios',
            field=models.CharField(max_length=500, verbose_name=b'Comentarios', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userstory',
            name='descripcion',
            field=models.CharField(max_length=500, verbose_name=b'Descripcion', blank=True),
            preserve_default=True,
        ),
    ]
