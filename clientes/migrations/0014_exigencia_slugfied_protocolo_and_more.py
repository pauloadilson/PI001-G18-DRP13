# Generated by Django 5.0.3 on 2024-04-24 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0013_alter_cliente_arquivo_do_cliente_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exigencia',
            name='slugfied_protocolo',
            field=models.SlugField(default=1, max_length=25, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recurso',
            name='slugfied_protocolo',
            field=models.SlugField(default=1, max_length=25, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requerimento',
            name='slugfied_NB',
            field=models.SlugField(default=1, max_length=25, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='requerimento',
            name='NB',
            field=models.CharField(default=1, max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
