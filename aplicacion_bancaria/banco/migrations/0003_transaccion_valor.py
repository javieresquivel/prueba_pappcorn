# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 23:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0002_auto_20170716_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaccion',
            name='valor',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
