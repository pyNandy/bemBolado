# Generated by Django 5.0 on 2024-11-25 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0006_alter_perfil_cep_alter_perfil_complemento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='complemento',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]