# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('flujo', '0001_initial'),
        ('auth', '0001_initial'),
        ('cliente', '0001_initial'),
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
                ('estado', models.CharField(default=b'Inactivo', max_length=15)),
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
        migrations.CreateModel(
            name='ProyectoFlujoActividad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estado', models.CharField(blank=True, max_length=5, editable=False, choices=[(b'ToDo', b'ToDo'), (b'Doing', b'Doing'), (b'Done', b'Done')])),
                ('flujoActividad', models.ForeignKey(to='flujo.FlujoActividad')),
                ('proyecto', models.ForeignKey(to='proyecto.Proyecto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, verbose_name=b'Nombre')),
                ('estado', models.TextField(default=b'Creado', max_length=10)),
                ('activo', models.BooleanField(default=True)),
                ('fechainicio', models.DateField(default=datetime.date.today, null=True, blank=True)),
                ('tiempoacumulado', models.IntegerField(default=0, blank=True)),
                ('fechafin', models.DateField(default=datetime.date.today)),
                ('duracion', models.PositiveIntegerField(default=0, blank=True)),
                ('proyecto', models.ForeignKey(to='proyecto.Proyecto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Userstory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, verbose_name=b'Nombre')),
                ('descripcion', models.TextField(max_length=100, verbose_name=b'Descripcion', blank=True)),
                ('tiempoestimado', models.IntegerField(default=0, verbose_name=b'Tiempo Estimado')),
                ('tiempotrabajado', models.IntegerField(default=0, null=True, verbose_name=b'Tiempo Trabajado', blank=True)),
                ('comentarios', models.TextField(max_length=100, verbose_name=b'Comentarios', blank=True)),
                ('estado', models.CharField(default=b'Nueva', max_length=10, verbose_name=b'Estado:', choices=[(b'Nueva', b'Nueva'), (b'InPlanning', b'InPlanning'), (b'EnCurso', b'EnCurso'), (b'Resuelta', b'Resuelta'), (b'Comentario', b'Comentario'), (b'Validado', b'Validado'), (b'Cancelado', b'Cancelado')])),
                ('prioridad', models.CharField(default=True, max_length=10, verbose_name=b'Prioridad: ', choices=[(b'Normal', b'Normal'), (b'Baja', b'Baja'), (b'Alta', b'Alta')])),
                ('porcentajerealizado', models.CharField(default=b'<0%>', max_length=10, verbose_name=b'Porcentaje Realizado: ', choices=[(b'0%', b'0%'), (b'10%', b'10%'), (b'20%', b'20%'), (b'30%', b'30%'), (b'40%', b'40%'), (b'50%', b'50%'), (b'60%', b'60%'), (b'70%', b'70%'), (b'80%', b'80%'), (b'90%', b'90%'), (b'100%', b'100%')])),
                ('historial', models.CharField(verbose_name=b'Historico', max_length=1000, editable=False, blank=True)),
                ('activo', models.BooleanField(default=True, editable=False)),
                ('sprint', models.ForeignKey(to='proyecto.Sprint')),
                ('usuarioasignado', models.ForeignKey(verbose_name=b'Asignado a: ', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='proyectoflujoactividad',
            name='userstory',
            field=models.ForeignKey(to='proyecto.Userstory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flujoproyecto',
            name='proyecto',
            field=models.ForeignKey(to='proyecto.Proyecto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flujoproyecto',
            name='sprint',
            field=models.ForeignKey(default=1, to='proyecto.Sprint'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='equipo',
            name='proyecto',
            field=models.ForeignKey(to='proyecto.Proyecto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='equipo',
            name='rol',
            field=models.ForeignKey(to='auth.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='equipo',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
