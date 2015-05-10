# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sprint', '0002_auto_20150501_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='fechafin',
            field=models.DateField(default=datetime.date(2015, 5, 9)),
            preserve_default=True,
        ),
    ]
