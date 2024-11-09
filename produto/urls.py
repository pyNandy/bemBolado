from django.urls import path
from . import views


app_name = 'produto'

urlpatterns = [
    path('', views.home, name="home"),
    path('lista', views.ListaProdutos.as_view(), name="lista"),
    path('<slug>', views.DetalheProduto.as_view(), name="detalhe"),
    path('adicionaraocarrinho/', views.AdicionarAoCarrinho.as_view(), name="adicionaraocarrinho"),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(), name="removerdocarrinho"),
    path('carrinho/', views.Carrinho.as_view(), name="carrinho"),
    path('resumodacompra/', views.ResumoDaCompra.as_view(), name="resumodacompra"),
    path('busca/', views.Busca.as_view(), name="busca"),
    path('bebidas/', views.lista_bebidas, name='lista_bebidas'),
    path('bebidas/<slug:slug>/', views.detalhe_bebida, name='detalhe_bebida'),
    path('doces/', views.lista_doces.as_view(), name='lista_doces'),
    path('doces/<slug:slug>/', views.DetalheDoce.as_view(), name='detalhe_doces'),
    path('buscar/', views.Buscar.as_view(), name='buscar_doces'),


]


