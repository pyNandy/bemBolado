from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from produto.models import Forma_Pagamento, Variacao, Borda
from .models import Pedido, ItemPedido
from utils import utils
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from perfil.models import Perfil
from django.utils.timezone import localtime
from decimal import Decimal
from notifications.signals import notify
from django.contrib.auth.models import User
from utils.utils import formata_preco
import json
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')
        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)
        return qs

class Pagar(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'

class Detalhe(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'pedido/detalhe.html'
    pk_url_kwarg = 'pk'

class Lista(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/lista.html'
    paginate_by = 10
    ordering = ['-id']
    
def gerar_pdf(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    usuario = pedido.usuario
    perfil = get_object_or_404(Perfil, usuario=usuario)  # Acessando o perfil do usuário
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=pedido_{pedido_id}.pdf'
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Estilo personalizado para título à esquerda
    title_style = ParagraphStyle(
        name='TitleLeft',
        parent=styles['Title'],
        alignment=0  # 0 para alinhamento à esquerda
    )

    # Título com número do pedido à esquerda
    title = f"Pedido: {pedido.id}"
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 12))

    # Reduzindo o tamanho da fonte
    small_style = styles['Normal']
    small_style.fontSize = 8

    # Valor em dinheiro e troco (se aplicável)
    valor_dinheiro = None
    troco = None
    if pedido.forma_pagamento.pagamento == 'Dinheiro':
        valor_dinheiro = pedido.valor_pagamento
        troco = Decimal(valor_dinheiro) - Decimal(pedido.total)

    # Dados do pedido com quebras de linha
    dados_pedido = f"""
    Criado em: {localtime(pedido.created_at).strftime('%d/%m/%Y %H:%M:%S')}<br/><br/>
    Status: {pedido.get_status_display()}<br/><br/>
    
    Cliente: {usuario.first_name} {usuario.last_name}<br/>
    Usuário: {usuario.username}<br/>
    Endereço: {perfil.endereco}, {perfil.numero}, {perfil.complemento}, {perfil.bairro}, {perfil.cidade} - {perfil.cep}<br/><br/>
    Forma de Pagamento: {pedido.forma_pagamento}<br/>
    Valor em Dinheiro: {formata_preco(valor_dinheiro) if valor_dinheiro is not None else 'N/A'}<br/>
    Troco: {formata_preco(troco) if troco is not None else 'N/A'}<br/><br/>
    Quantidade Total: {pedido.qtd_total}<br/>
    Total a Pagar: {pedido.get_total_formatado()}
    """
    elements.append(Paragraph(dados_pedido, small_style))
    elements.append(Spacer(1, 12))
    elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.black))

    # Itens do pedido
    elements.append(Spacer(1, 12))
    for item in ItemPedido.objects.filter(pedido=pedido):
        item_info = f"""
        Qtde.: {item.quantidade}  |
        Produto: {item.produto}  |
        Tamanho: {item.variacao}  |
        Borda: {item.borda.nome if item.borda else 'N/A'}  |
        Preço: {item.get_precoPedido_formatado()}  |
        Preço Promocional: {item.get_precoPedidoPromo_formatado()}
        """
        elements.append(Paragraph(item_info, small_style))
        elements.append(Spacer(1, 12))
        elements.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', color=colors.grey))

    doc.build(elements)
    return response


def finalizar_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    pedido.status = 'finalizado'
    pedido.save()

    # Enviando notificação para superusuários
    superusers = User.objects.filter(is_superuser=True)
    for superuser in superusers:
        notify.send(request.user, recipient=superuser, verb=f"Pedido {pedido.id} foi finalizado")

    return HttpResponse('Pedido finalizado')


class SalvarPedido(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Você precisa fazer login.')
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(self.request, 'Seu carrinho está vazio.')
            return redirect('produto:lista')

        return redirect('produto:resumo_da_compra')

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(self.request, 'Carrinho vazio.')
            return redirect('produto:lista')

        forma_pagamento_id = self.request.POST.get('forma_pagamento')
        valor_pagamento_str = self.request.POST.get('valor_pagamento', '0').replace(',', '.')
        try:
            forma_pagamento = Forma_Pagamento.objects.get(id=forma_pagamento_id)
        except Forma_Pagamento.DoesNotExist:
            messages.error(self.request, 'Forma de pagamento inválida.')
            return render(self.request, 'produto/resumodacompra.html')

        valor_dinheiro = None
        if forma_pagamento.pagamento == 'Dinheiro':
            try:
                valor_dinheiro = float(valor_pagamento_str)
            except ValueError:
                messages.error(self.request, 'Digite um valor válido em formato de moeda (ex: 15,00 ou 25,15).')
                return render(self.request, 'produto/resumodacompra.html')

        carrinho = self.request.session.get('carrinho', {})
        if isinstance(carrinho, str):
            carrinho = json.loads(carrinho)

        qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        valor_total_carrinho = utils.cart_totals(carrinho)

        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='P',
            forma_pagamento=forma_pagamento,
            valor_pagamento=valor_dinheiro
        )

        pedido.save()

        item_pedido_objs = []
        for v in carrinho.values():
            borda = None
            if 'borda_nome' in v:
                borda = Borda.objects.filter(nome=v['borda_nome']).first()
            item_pedido_objs.append(
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promocional=v['preco_quantitativo_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                    borda=borda,
                )
            )
        
        ItemPedido.objects.bulk_create(item_pedido_objs)

        troco = None
        if valor_dinheiro is not None:
            troco = valor_dinheiro - float(pedido.total)

        contexto = {
            'pedido': pedido,
            'itens_pedido': item_pedido_objs,
            'troco': utils.formata_preco(troco) if troco is not None else None,
            'valor_total_produto': utils.formata_preco(pedido.total),
            'valor_dinheiro': utils.formata_preco(valor_dinheiro) if valor_dinheiro is not None else None,
            'forma_pagamento_selecionada': forma_pagamento,
            'carrinho': carrinho
        }

        # Limpar o carrinho da sessão
        del self.request.session['carrinho']
    
        # Enviar notificação ao superusuário
        superusers = User.objects.filter(is_superuser=True)
        for superuser in superusers:
            notify.send(self.request.user, recipient=superuser, verb=f"Pedido {pedido.id} foi finalizado")

        # Enviar e-mails para o cliente e superusuários
        subject = f'Pedido {pedido.id} Finalizado'
        html_message = render_to_string('pedido/email_template.html', {'pedido': pedido})
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.request.user.email]
        
        # Enviar e-mail para o cliente
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

        # Enviar e-mail para superusuários
        superuser_emails = [user.email for user in superusers]
        send_mail(subject, plain_message, from_email, superuser_emails, html_message=html_message)

        return render(self.request, self.template_name, contexto)
