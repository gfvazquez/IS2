# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actividades',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, verbose_name=b'Nombre:')),
                ('estado', models.CharField(blank=True, max_length=5, editable=False, choices=[(b'ToDo', b'ToDo'), (b'Doing', b'Doing'), (b'Done', b'Done')])),
                ('is_active', models.BooleanField(default=True, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
