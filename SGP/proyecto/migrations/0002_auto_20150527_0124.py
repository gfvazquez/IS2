# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proyecto',
            options={'ordering': ['nombre'], 'permissions': (('asignar_equipo', 'Puede asignar un usuario al proyecto'), ('asignar_flujo', 'Puede asignar un flujo al proyecto'), ('asignar_sprint', 'Puede asignar un Sprint a un Flujo-Proyecto'), ('reasignar_sprint', 'puede reasignar un Sprint a un Flujo-Proyecto'))},
        ),
    ]
