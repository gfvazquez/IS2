# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sprint', '0006_auto_20150512_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='fechainicio',
            field=models.DateField(default=datetime.date.today, null=True, blank=True),
            preserve_default=True,
        ),
    ]
