# Generated by Django 5.0.3 on 2024-05-01 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0015_alter_cliente_arquivo_do_cliente_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exigencia',
            name='slugfied_protocolo',
        ),
        migrations.RemoveField(
            model_name='recurso',
            name='slugfied_protocolo',
        ),
        migrations.RemoveField(
            model_name='requerimento',
            name='slugfied_NB',
        ),
    ]
