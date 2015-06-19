# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0004_auto_20150528_2349'),
    ]

    operations = [
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, verbose_name=b'Nombre')),
                ('proyecto', models.ForeignKey(to='proyecto.Proyecto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReleaseUsValidados',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('release', models.ForeignKey(to='proyecto.Release')),
                ('userstory', models.ForeignKey(to='proyecto.Userstory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
