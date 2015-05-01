# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sprint', '0001_initial'),
        ('userstory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstory',
            name='sprint',
            field=models.ForeignKey(default=1, to='sprint.Sprint'),
            preserve_default=False,
        ),
    ]
