# Generated by Django 5.0.3 on 2024-04-06 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0008_recurso_natureza'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Exigência',
            new_name='Exigencia',
        ),
        migrations.RemoveField(
            model_name='recurso',
            name='natureza',
        ),
    ]
