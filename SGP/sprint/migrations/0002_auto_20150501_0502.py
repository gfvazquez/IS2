# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sprint', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='fechafin',
            field=models.DateField(default=datetime.date(2015, 5, 1)),
            preserve_default=True,
        ),
    ]
