# Generated by Django 5.0.6 on 2024-06-06 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar_intercambiador', '0028_alter_intercambiador_imagen_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='ayudante',
            name='imagen_perfil',
            field=models.ImageField(default='./static/perfil_default.jpg', upload_to=''),
        ),
    ]
