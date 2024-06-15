# Generated by Django 5.0.6 on 2024-05-27 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar_intercambiador', '0019_alter_intercambiador_correo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Intercambio',
            fields=[
                ('id_intercambio', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('fecha_concretada', models.DateTimeField()),
                ('fecha_oferta', models.DateTimeField()),
                ('estado', models.CharField(choices=[('ofertado', 'Ofertado'), ('pendiente', 'Pendiente'), ('cancelado', 'Cancelado'), ('realizado', 'Realizado')], default='ofertado', max_length=20)),
                ('filial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registrar_intercambiador.filial')),
                ('publi_ofertada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ofertada_intercambio', to='registrar_intercambiador.publicacion')),
                ('publi_recibida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recibida_intercambio', to='registrar_intercambiador.publicacion')),
            ],
        ),
    ]
