from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from .models import Bebida, Forma_Pagamento, Produto_3, Borda, Alteracao, VariacaoBebida
from . import models
from perfil.models import Perfil
import logging
from pprint import pprint
from pedido.models import Pedido
from utils import utils
from utils.utils import formata_preco

# Configuração básica do logging
logging.basicConfig(level=logging.DEBUG)

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 12
    ordering = ['-id']


class Busca(ListaProdutos):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo') or self.request.session['termo']
        qs = super().get_queryset(*args, **kwargs)

        if not termo:
            return qs

        self.request.session['termo'] = termo

        qs = qs.filter(
            Q(nome__icontains=termo) |
            Q(descricao_curta__icontains=termo) |
            Q(descricao_longa__icontains=termo)
        )

        self.request.session.save()
        return qs


logger = logging.getLogger(__name__)

class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        
        # Verifica todos os conjuntos de parâmetros
        variacao_id = self.request.GET.get('vid') or self.request.GET.get('doc') or self.request.GET.get('bil')
        borda_id = self.request.GET.get('bid') or self.request.GET.get('loc')
        produto_tipo = self.request.GET.get('tipo', '1')  # Tipo de produto (1 para Produto, 2 para Produto_3, 3 para Bebida)

        logger.debug(f"variacao_id: {variacao_id}, borda_id: {borda_id}, produto_tipo: {produto_tipo}")

        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)

        try:
            if produto_tipo == '1':
                variacao = get_object_or_404(models.Variacao, id=variacao_id)
            elif produto_tipo == '2':
                variacao = get_object_or_404(models.Alteracao, id=variacao_id)
            elif produto_tipo == '3':
                variacao = get_object_or_404(models.VariacaoBebida, id=variacao_id)
            else:
                messages.error(
                    self.request,
                    'Tipo de produto inválido'
                )
                return redirect(http_referer)
        except models.Variacao.DoesNotExist:
            messages.error(
                self.request,
                'Variação não encontrada'
            )
            return redirect(http_referer)
        except models.Alteracao.DoesNotExist:
            messages.error(
                self.request,
                'Alteração não encontrada'
            )
            return redirect(http_referer)
        except models.VariacaoBebida.DoesNotExist:
            messages.error(
                self.request,
                'Variação de bebida não encontrada'
            )
            return redirect(http_referer)

        variacao_estoque = variacao.estoque if produto_tipo == '1' else variacao.estoque_3 if produto_tipo == '2' else variacao.estoque_b
        produto = variacao.produto if produto_tipo == '1' else variacao.produto if produto_tipo == '2' else variacao.produto_b

        borda = get_object_or_404(models.Borda, id=borda_id) if borda_id else None

        produto_id = produto.id
        produto_nome = produto.nome if produto_tipo == '1' else produto.nome_produto_3 if produto_tipo == '2' else produto.nome_b
        variacao_nome = variacao.nome if produto_tipo == '1' else variacao.nome_variacao if produto_tipo == '2' else variacao.nome_b or ''
        preco_unitario = variacao.preco if produto_tipo == '1' else variacao.preco_venda if produto_tipo == '2' else variacao.preco_marketing_b
        preco_unitario_promocional = variacao.preco_promocional if produto_tipo == '1' else variacao.preco_venda_promocional if produto_tipo == '2' else variacao.preco_promocional_b
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem
        borda_nome = borda.nome if borda else ''

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao_estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no '
                    f'produto "{produto_nome}". Adicionamos {variacao_estoque}x '
                    f'no seu carrinho.'
                )
                quantidade_carrinho = variacao_estoque

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho
        else:
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem,
                'borda_nome': borda_nome,
            }

        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {produto_nome} {variacao_nome} adicionado ao seu '
            f'carrinho {carrinho[variacao_id]["quantidade"]}x.'
        )

        return redirect(http_referer)

class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)

        carrinho = self.request.session['carrinho'][variacao_id]

        messages.success(
            self.request,
            f'Produto {carrinho["produto_nome"]} {carrinho["variacao_nome"]} '
            f'removido do seu carrinho.'
        )

        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        return redirect(http_referer)


class Carrinho(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {})
        }

        return render(self.request, 'produto/carrinho.html', contexto)


class lista_doces(ListView):
    model = models.Produto_3
    template_name = 'produto/lista_doces.html'
    context_object_name = 'produtos'
    paginate_by = 12
    ordering = ['-id']

    
class Buscar(lista_doces):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo')
        
        # Salva o termo na sessão se ele foi passado na URL
        if termo:
            self.request.session['termo'] = termo
        else:
            # Verifica se o termo já está na sessão
            termo = self.request.session.get('termo', None)
        
        qs = super().get_queryset(*args, **kwargs)
        
        # Se ainda não tiver termo, retorna a queryset original
        if not termo:
            return qs
        
        # Filtra a queryset com base no termo
        qs = qs.filter(
            Q(nome_produto_3__icontains=termo) |
            Q(descricao_venda_curta__icontains=termo) |
            Q(descricao_venda_longa__icontains=termo)
        )
        
        return qs


def lista_bebidas(request):
    bebidas = Bebida.objects.all()
    return render(request, 'produto/lista_bebidas.html', {'bebidas': bebidas})

def detalhe_bebida(request, slug):
    bebida = get_object_or_404(Bebida, slug=slug)
    return render(request, 'produto/detalhe_bebida.html', {'bebida': bebida})



class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class DetalheDoce(DetailView):
    model = models.Produto_3
    template_name = 'produto/detalhe_doce.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bordas'] = models.Borda.objects.filter(object_id=self.object.id)
        return context

class DetalheBebida(DetailView):
    model = models.Bebida
    template_name = 'produto/detalhe_bebida.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

from django.shortcuts import render

def doces_view(request, slug):
    # lógica da view
    return render(request, 'detalhe_doce.html', {'slug': slug})


class Pagar(View):
    def get(self, request, pk, *args, **kwargs):
        pedido = get_object_or_404(Pedido, pk=pk)
        contexto = {
            'pedido': pedido,
        }
        return render(request, 'pedido/pagar.html', contexto)
    

class ResumoDaCompra(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        if not Perfil.objects.filter(usuario=self.request.user).exists():
            messages.error(self.request, 'Cadastro incompleto, atualize seus dados a seguir para concluir seu Pedido!!.')
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(self.request, 'Carrinho vazio.')
            return redirect('produto:lista')

        tipos_pagamento = Forma_Pagamento.objects.all()
        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho'],
            'tipos': tipos_pagamento
        }
        return render(self.request, 'produto/resumodacompra.html', contexto)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        if not Perfil.objects.filter(usuario=self.request.user).exists():
            messages.error(self.request, 'Seu Cadastro está incompleto, atualize seus dados ao lado para concluir seu Pedido!!!.')
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(self.request, 'Carrinho vazio.')
            return redirect('produto:lista')

        forma_pagamento_id = self.request.POST.get('forma_pagamento')
        valor_pagamento = self.request.POST.get('valor_pagamento')

        return redirect(reverse('pedido:salvarpedido') + f'?forma_pagamento={forma_pagamento_id}&valor_pagamento={valor_pagamento}')
    

def home(request):
    #logica views
    return render(request, 'produto/home.html')
