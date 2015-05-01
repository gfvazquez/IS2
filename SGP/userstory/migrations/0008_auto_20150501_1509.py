# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userstory', '0007_auto_20150501_0354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='estado',
            field=models.CharField(default=b'Nueva', max_length=10, verbose_name=b'Estado:', choices=[(b'Nueva', b'Nueva'), (b'InPlanning', b'InPlanning'), (b'EnCurso', b'EnCurso'), (b'Resuelta', b'Resuelta'), (b'Comentarios', b'Comentarios'), (b'Validado', b'Validado'), (b'Cancelado', b'Cancelado')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userstory',
            name='historial',
            field=models.CharField(verbose_name=b'Historico', max_length=1000, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
