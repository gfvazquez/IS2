# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proyecto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipo',
            name='rol',
            field=models.ForeignKey(default=16, to='auth.Group'),
            preserve_default=False,
        ),
    ]