# Generated by Django 5.0.6 on 2024-05-17 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar_intercambiador', '0003_categoria_filial_alter_ayudante_dni_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ayudante',
            name='correo',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
