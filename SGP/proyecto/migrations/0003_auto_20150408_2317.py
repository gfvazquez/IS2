# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flujo', '0002_auto_20150402_2353'),
        ('proyecto', '0002_auto_20150408_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlujoProyecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flujo', models.ForeignKey(to='flujo.Flujo')),
                ('proyecto', models.ForeignKey(to='proyecto.Proyecto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='proyecto',
            options={},
        ),
    ]
