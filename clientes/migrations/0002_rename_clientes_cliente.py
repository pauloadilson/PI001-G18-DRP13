# Generated by Django 5.0.3 on 2024-03-29 00:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Clientes',
            new_name='Cliente',
        ),
    ]