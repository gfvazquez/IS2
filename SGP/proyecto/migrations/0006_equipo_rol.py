# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('proyecto', '0005_auto_20150410_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipo',
            name='rol',
            field=models.ForeignKey(default=3, to='auth.Group'),
            preserve_default=False,
        ),
    ]
