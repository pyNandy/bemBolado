# Generated by Django 5.0 on 2024-10-17 11:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0005_alter_produto_tipo_borda'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produto_3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_produto_3', models.CharField(max_length=255, verbose_name='Produtos')),
                ('descricao_venda_curta', models.TextField(max_length=255, verbose_name='Descr.Produto')),
                ('descricao_venda_longa', models.TextField(verbose_name='Detalhes do Produto')),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='produto_imagens/%Y/%m/')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('preco_de_venda', models.FloatField(verbose_name='Preço')),
                ('preco_de_venda_promocional', models.FloatField(default=0, verbose_name='Preço Promo.')),
                ('tipo', models.CharField(choices=[('V', 'Variável'), ('S', 'Simples')], default='V', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Variacao_2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_variacao', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tamanho')),
                ('preco_venda', models.FloatField()),
                ('preco_venda_promocional', models.FloatField(default=0)),
                ('estoque_3', models.PositiveIntegerField(default=1, verbose_name='Estoque')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produto.produto_3', verbose_name='Produto')),
            ],
            options={
                'verbose_name': 'Variação 2',
                'verbose_name_plural': 'Variações 2',
            },
        ),
    ]
