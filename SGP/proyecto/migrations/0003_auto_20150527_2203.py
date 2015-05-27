# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proyecto', '0002_auto_20150527_0124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='usuarios_proyecto',
        ),
        migrations.AddField(
            model_name='proyecto',
            name='scrum_master',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
