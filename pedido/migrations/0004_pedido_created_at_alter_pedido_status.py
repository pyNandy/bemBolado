from django.db import migrations, models
import django.utils.timezone

def set_default_datetime(apps, schema_editor):
    Pedido = apps.get_model('pedido', 'Pedido')
    for pedido in Pedido.objects.all():
        pedido.created_at = django.utils.timezone.now()
        pedido.save()

class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0003_itempedido_borda'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.RunPython(set_default_datetime),
    ]

