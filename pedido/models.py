from django.db import models
from django.contrib.auth.models import User
from utils import utils
from django.utils import timezone
from produto.models import Forma_Pagamento, Borda
from .models import Forma_Pagamento 


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    qtd_total = models.PositiveIntegerField(verbose_name='Qtde. Total')
    status = models.CharField(
        default="C",
        max_length=1,
        choices=(
            ('A', 'Aprovado'),
            ('C', 'Em preparação'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Saiu para Entrega'),
            ('F', 'Finalizado'),
        )
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Criado em')
    forma_pagamento = models.ForeignKey(Forma_Pagamento, on_delete=models.SET_NULL, null=True)
    valor_pagamento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Adicionado

    def get_total_formatado(self):
        return utils.formata_preco(self.total)
    get_total_formatado.short_description = 'Vlr. Total'

    def __str__(self):
        return f'Pedido N. {self.pk}'



class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, verbose_name='Número do Pedido')
    produto = models.CharField(max_length=255)
    variacao = models.CharField(max_length=255, verbose_name='Tamanho')
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    preco_promocional = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantidade = models.PositiveIntegerField()
    produto_id = models.PositiveIntegerField()
    variacao_id = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2000)
    borda = models.ForeignKey(Borda, on_delete=models.SET_NULL, null=True, blank=True)  # Adicionando o campo 'borda'

    def __str__(self):
        return f'Item do {self.pedido}'

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'

    def get_precoPedido_formatado(self):
        return utils.formata_preco(self.preco)
    get_precoPedido_formatado.short_description = 'Preço'

    def get_precoPedidoPromo_formatado(self):
        return utils.formata_preco(self.preco_promocional)
    get_precoPedidoPromo_formatado.short_description = 'Preço Promocional'
