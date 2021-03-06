# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-16 15:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('estado_registro', models.BooleanField(default=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('codigo', models.CharField(max_length=4, unique=True)),
                ('nombre', models.CharField(max_length=250)),
                ('direccion', models.CharField(max_length=250)),
                ('usuario_registro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('estado_registro', models.BooleanField(default=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('documento', models.CharField(max_length=50, unique=True)),
                ('nombre', models.CharField(max_length=250)),
                ('direccion', models.CharField(max_length=250)),
                ('fecha_nacimiento', models.DateField()),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banco.Banco')),
                ('usuario_registro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('estado_registro', models.BooleanField(default=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('tipo', models.SmallIntegerField(choices=[(1, 'Corriente'), (2, 'Ahorros'), (3, 'Otra')], default=2)),
                ('numero_cuenta', models.CharField(max_length=30)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banco.Cliente')),
                ('usuario_registro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TarjetaDebito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('estado_registro', models.BooleanField(default=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('numero', models.CharField(max_length=30)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banco.Cuenta')),
                ('usuario_registro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('estado_registro', models.BooleanField(default=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('tipo', models.SmallIntegerField(choices=[(1, 'Transeferencia'), (2, 'Consignaci\xf3n'), (3, 'Retiro')])),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banco.Banco')),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuenta', to='banco.Cuenta')),
                ('cuenta_destino', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cuenta_destino', to='banco.Cuenta')),
                ('usuario_registro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
