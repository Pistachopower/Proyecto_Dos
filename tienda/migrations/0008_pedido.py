# Generated by Django 5.1.7 on 2025-05-08 11:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0007_delete_pedido'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('P', 'Pendiente'), ('C', 'Completado'), ('A', 'Anulado')], default='P', max_length=1)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('direccion', models.CharField(max_length=100)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.cliente')),
                ('pieza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.pieza')),
            ],
        ),
    ]
