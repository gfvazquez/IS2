# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userstory', '0005_auto_20150501_0339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='descripcion',
            field=models.TextField(max_length=50, verbose_name=b'Descripcion', blank=True),
            preserve_default=True,
        ),
    ]
