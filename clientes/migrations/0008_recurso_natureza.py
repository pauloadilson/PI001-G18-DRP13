# Generated by Django 5.0.3 on 2024-04-06 19:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0007_natureza_exigência_recurso'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurso',
            name='natureza',
            field=models.ForeignKey(default=123456, on_delete=django.db.models.deletion.PROTECT, related_name='natureza_recurso', to='clientes.natureza'),
            preserve_default=False,
        ),
    ]
