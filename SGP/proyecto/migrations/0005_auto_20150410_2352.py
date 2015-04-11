# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0004_proyecto_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='descripcion',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
