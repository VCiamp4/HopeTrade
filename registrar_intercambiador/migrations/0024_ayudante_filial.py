# Generated by Django 5.0.6 on 2024-05-30 14:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar_intercambiador', '0023_alter_intercambio_fecha_concretada'),
    ]

    operations = [
        migrations.AddField(
            model_name='ayudante',
            name='filial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registrar_intercambiador.filial'),
        ),
    ]
