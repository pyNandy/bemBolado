from django.shortcuts import get_object_or_404
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from . import models
from .models import ItemPedido, Pedido

# Definindo as tabelas do SuperUser - ITENS DO PEDIDO
class ItemPedidoInline(admin.TabularInline):
    model = models.ItemPedido
    extra = 1

class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = [
        'pedido', 'quantidade', 'produto', 'borda', 'variacao',
        'get_precoPedido_formatado', 'get_precoPedidoPromo_formatado'
    ]

# Classe para configuração do Pedido no admin
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['numero_do_pedido', 'usuario', 'status', 'qtd_total', 'get_total_formatado', 'download_pdf_link', 'created_at',"forma_pagamento"]
    inlines = [ItemPedidoInline]

    def numero_do_pedido(self, obj):
        return obj.id
    numero_do_pedido.short_description = 'Número do Pedido'

    def download_pdf_link(self, obj):
        url = reverse('pedido:gerar_pdf', args=[obj.id])
        return format_html('<a href="{}">Baixar Pedido</a>', url)
    download_pdf_link.short_description = 'Download PDF'

    def created_at(self, obj):
        return obj.created_at.strftime('%d/%m/%Y %H:%M:%S')
    created_at.short_description = 'Criado em'

    def get_total_formatado(self, obj):
        return obj.get_total_formatado()
    get_total_formatado.short_description = 'Vlr. Total'

admin.site.register(models.Pedido, PedidoAdmin)
admin.site.register(models.ItemPedido, ItemPedidoAdmin)
