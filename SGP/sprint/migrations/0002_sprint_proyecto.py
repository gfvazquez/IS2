# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0001_initial'),
        ('sprint', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='proyecto',
            field=models.ForeignKey(default=1, to='proyecto.Proyecto'),
            preserve_default=False,
        ),
    ]