# Generated by Django 5.0.6 on 2024-05-30 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar_intercambiador', '0022_alter_publicacion_estado_publicacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intercambio',
            name='fecha_concretada',
            field=models.DateTimeField(null=True),
        ),
    ]
