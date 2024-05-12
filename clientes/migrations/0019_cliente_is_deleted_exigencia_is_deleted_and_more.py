# Generated by Django 5.0.3 on 2024-05-08 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0018_rename_data_exigencia_data_final_prazo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='exigencia',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recurso',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='requerimento',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]