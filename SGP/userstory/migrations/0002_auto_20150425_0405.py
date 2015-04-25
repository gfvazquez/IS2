# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userstory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='comentarios',
            field=models.TextField(null=True, verbose_name=b'Comentarios'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userstory',
            name='descripcion',
            field=models.TextField(null=True, verbose_name=b'Descripcion'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userstory',
            name='porcentajerealizado',
            field=models.CharField(default=b'<0%>', max_length=10, choices=[(b'0%', b'0%'), (b'10%', b'10%'), (b'20%', b'20%'), (b'30%', b'30%'), (b'40%', b'40%'), (b'50%', b'50%'), (b'60%', b'60%'), (b'70%', b'70%'), (b'80%', b'80%'), (b'90%', b'90%'), (b'100%', b'100%')]),
            preserve_default=True,
        ),
    ]
