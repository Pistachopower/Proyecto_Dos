# Generated by Django 5.1.9 on 2025-06-08 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0023_pedido_tienda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devolucion',
            name='estado',
            field=models.CharField(choices=[('P', 'Pendiente'), ('R', 'Resuelta'), ('D', 'Denegada')], default='P', max_length=1),
        ),
    ]
