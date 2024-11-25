# Generated by Django 5.0 on 2024-11-04 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0007_pedido_forma_pagamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='valor_pagamento',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
