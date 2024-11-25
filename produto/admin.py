from django.contrib import admin
from .forms import VariacaoObrigatoria
from . import models
import csv
from django.http import HttpResponse
import pandas as pd

from django.contrib.contenttypes.admin import GenericStackedInline


class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    formset = VariacaoObrigatoria
    min_num = 1
    extra = 0
    can_delete = True


# class BordaInline(admin.TabularInline):
class BordaInline(GenericStackedInline):
    model = models.Borda
    min_num = 1
    extra = 0
    can_delete = True

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao_curta', 'descricao_longa', 'get_preco_formatado', 'get_preco_promocional_formatado']
    search_fields =['nome']
    list_filter =  ['nome']
    inlines = [
        VariacaoInline,
        BordaInline         
    ]

    def get_produto_nome(self, obj):
        return obj.nome
    get_produto_nome.admin_order_field = 'nome'
    get_produto_nome.short_description = 'Nome do Produto'


    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Produtos.csv"'
        writer = csv.writer(response)
        writer.writerow(['Produto', 'Descricao Curta', 'Descrição Longa', 'Preço Marketing', 'Preço Promocional'])
        for produtos in queryset:
            writer.writerow([produtos.nome, produtos.descricao_curta, produtos.descricao_longa, produtos.get_preco_formatado(), 
                             produtos.get_preco_promocional_formatado()])
        return response

    def export_to_excel(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Produtos.xlsx"'
        
        data = []
        for produtos in queryset:
            data.append([produtos.nome, produtos.descricao_curta, produtos.descricao_longa, produtos.get_preco_formatado(),produtos.get_preco_promocional_formatado()])

        df = pd.DataFrame(data, columns=['Produto', 'Descr.Produto', 'Detalhes Produto', 'Preço Marketing', 'Preço Promocional'])
        
        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Variacoes', index=False)
        
        return response

    export_to_csv.short_description = 'Exportar para CSV'
    export_to_excel.short_description = 'Exportar para Excel'
    actions = [export_to_csv, export_to_excel]

class VariacaoAdmin(admin.ModelAdmin):
    list_display = ['produto', 'nome', 'get_preco_variacao_formatado', 'get_preco_promocional_variacao_formatado', 'estoque']

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Variacoes.csv"'
        writer = csv.writer(response)
        writer.writerow(['Produto', 'Tamanho', 'Preço', 'Preço Promocional', 'Estoque'])
        for variacao in queryset:
            writer.writerow([variacao.produto, variacao.nome, variacao.get_preco_variacao_formatado(), 
                             variacao.get_preco_promocional_variacao_formatado(), variacao.estoque])
        return response

    def export_to_excel(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Variacoes.xlsx"'
        
        data = []
        for variacao in queryset:
            data.append([variacao.produto, variacao.nome, variacao.get_preco_variacao_formatado(), 
                         variacao.get_preco_promocional_variacao_formatado(), variacao.estoque])
        
        df = pd.DataFrame(data, columns=['Produto', 'Tamanho', 'Preço', 'Preço Promocional', 'Estoque'])
        
        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Variacoes', index=False)
        
        return response

    export_to_csv.short_description = 'Exportar para CSV'
    export_to_excel.short_description = 'Exportar para Excel'
    actions = [export_to_csv, export_to_excel]

class VariacaoBebidaInline(admin.TabularInline):
    model = models.VariacaoBebida
    min_num = 1
    extra = 0
    can_delete = True

class BebidaAdmin(admin.ModelAdmin):
    list_display = ['nome_b', 'informacao_curta', 'informacao_longa', 'get_preco_bebida_formatado', 'get_preco_promocional_bebida_formatado']
    inlines = [
        VariacaoBebidaInline
    ]

class BordaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco']
    search_fields = ['nome']


class AlteracaoInline(admin.TabularInline):
    model = models.Alteracao
    min_num = 1
    extra = 1
    can_delete = True


class Produto_3Admin(admin.ModelAdmin):
    list_display = ['nome_produto_3', 'descricao_venda_curta', 'descricao_venda_longa', 'get_preco_venda_formatado', 'get_preco_venda_promocional_formatado']
    inlines = [
        AlteracaoInline,
        BordaInline,
    ]

    def get_produto_nome(self, obj):
        return obj.nome_produto_3
    get_produto_nome.admin_order_field = 'nome_produto_3'
    get_produto_nome.short_description = 'Nome do Produto'


class AlteracaoAdmin(admin.ModelAdmin):
    list_display = ['produto', 'nome_variacao', 'get_preco_variacao_venda_formatado', 'get_preco_promocional_variacao_venda_formatado', 'estoque_3']



admin.site.register(models.Produto, ProdutoAdmin)
admin.site.register(models.Variacao, VariacaoAdmin)
admin.site.register(models.Bebida, BebidaAdmin)
admin.site.register(models.Borda, BordaAdmin)
admin.site.register(models.Produto_3, Produto_3Admin)
admin.site.register(models.Alteracao, AlteracaoAdmin)
admin.site.register(models.Forma_Pagamento)