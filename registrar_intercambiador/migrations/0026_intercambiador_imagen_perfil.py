# Generated by Django 5.0.6 on 2024-06-06 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar_intercambiador', '0025_alter_publicacion_estado_publicacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='intercambiador',
            name='imagen_perfil',
            field=models.ImageField(default='/static/logo.png', upload_to=''),
        ),
    ]
