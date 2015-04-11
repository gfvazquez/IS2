# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_cliente_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='ruc',
            field=models.CharField(unique=True, max_length=20, verbose_name=b'Ruc'),
            preserve_default=True,
        ),
    ]
