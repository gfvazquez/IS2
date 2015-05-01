# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flujo', '0003_flujoactividad'),
    ]

    operations = [
        migrations.AddField(
            model_name='flujo',
            name='is_active',
            field=models.BooleanField(default=True, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flujo',
            name='estado',
            field=models.CharField(blank=True, max_length=5, editable=False, choices=[(b'Doing', b'Doing'), (b'Done', b'Done')]),
            preserve_default=True,
        ),
    ]
