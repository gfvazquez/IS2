# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_auto_20150410_2344'),
        ('auth', '0001_initial'),
        ('flujo', '0002_auto_20150402_2353'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FlujoProyecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flujo', models.ForeignKey(to='flujo.Flujo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('auto_increment_id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=30)),
                ('estado', models.CharField(default=b'Iniciado', max_length=15, choices=[(b'Iniciado', b'Iniciado'), (b'Finalizado', b'Finalizado'), (b'Cancelado', b'Cancelado')])),
                ('fecha_inicio', models.DateField()),
                ('duracion_estimada', models.IntegerField()),
                ('descripcion', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('cliente', models.ForeignKey(to='cliente.Cliente')),
                ('usuarios_proyecto', models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='proyecto.Equipo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='flujoproyecto',
            name='proyecto',
            field=models.ForeignKey(to='proyecto.Proyecto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='equipo',
            name='proyecto',
            field=models.ForeignKey(to='proyecto.Proyecto'),
            preserve_default=True,
        ),
        #migrations.AddField(
        #    model_name='equipo',
        #    name='rol',
        #    field=models.ForeignKey(to='auth.Group'),
        #    preserve_default=True,
        #),
        migrations.AddField(
            model_name='equipo',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
