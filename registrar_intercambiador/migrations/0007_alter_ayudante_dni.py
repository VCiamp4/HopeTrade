# Generated by Django 5.0.6 on 2024-05-17 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar_intercambiador', '0006_ayudante_groups_ayudante_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ayudante',
            name='dni',
            field=models.PositiveIntegerField(editable=False, primary_key=True, serialize=False),
        ),
    ]
