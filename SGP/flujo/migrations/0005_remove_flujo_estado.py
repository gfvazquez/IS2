# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flujo', '0004_auto_20150501_1338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flujo',
            name='estado',
        ),
    ]
