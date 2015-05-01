# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userstory', '0006_auto_20150501_0352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='comentarios',
            field=models.TextField(max_length=100, verbose_name=b'Comentarios', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userstory',
            name='descripcion',
            field=models.TextField(max_length=100, verbose_name=b'Descripcion', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userstory',
            name='historial',
            field=models.TextField(verbose_name=b'Historico', max_length=1000, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
