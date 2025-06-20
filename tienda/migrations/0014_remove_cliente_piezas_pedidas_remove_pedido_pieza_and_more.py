# Generated by Django 5.1.7 on 2025-05-15 10:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0013_alter_pedido_fecha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='piezas_pedidas',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='pieza',
        ),
        migrations.CreateModel(
            name='LineaPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.FloatField(default=1.0)),
                ('cantidad', models.IntegerField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedido_lineaPedido', to='tienda.pedido')),
                ('pieza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pieza_lineaPedido', to='tienda.pieza')),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tienda_lineaPedido', to='tienda.tienda')),
            ],
        ),
    ]
