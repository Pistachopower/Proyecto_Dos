# Generated by Django 5.1.7 on 2025-05-15 11:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0015_remove_pedido_direccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='direccion',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
