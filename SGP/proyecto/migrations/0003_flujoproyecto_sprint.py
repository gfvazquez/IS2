# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sprint', '0002_auto_20150510_0312'),
        ('proyecto', '0002_equipo_rol'),
    ]

    operations = [
        migrations.AddField(
            model_name='flujoproyecto',
            name='sprint',
            field=models.ForeignKey(default=1, to='sprint.Sprint'),
            preserve_default=True,
        ),
    ]
