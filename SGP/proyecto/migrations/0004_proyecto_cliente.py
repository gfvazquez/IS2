# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_cliente_estado'),
        ('proyecto', '0003_auto_20150408_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='cliente',
            field=models.ForeignKey(default=1, to='cliente.Cliente'),
            preserve_default=False,
        ),
    ]
