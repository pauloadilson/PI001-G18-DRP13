# Generated by Django 5.0.3 on 2024-04-22 23:43

import clientes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0011_cliente_arquivo_do_cliente_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requerimento',
            name='arquivo_do_requerimento',
            field=models.FileField(blank=True, null=True, upload_to=clientes.models.path_and_rename),
        ),
    ]
