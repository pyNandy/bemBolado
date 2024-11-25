from django.urls import path
from . import views
from .views import gerar_pdf

app_name = 'pedido'

urlpatterns = [
    path('pagar/<int:pk>', views.Pagar.as_view(), name='pagar'),
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedido'),
    path('lista/', views.Lista.as_view(), name='lista'),
    path('detalhe/<int:pk>', views.Detalhe.as_view(), name='detalhe'),
    
    path('pedido/<int:pedido_id>/pdf/', gerar_pdf, name='gerar_pdf'),
    path('<int:pedido_id>/pdf/', gerar_pdf, name='gerar_pdf'),
    path('finalizar_pedido/<int:pedido_id>/', views.finalizar_pedido, name="finalizar_pedido"),
    
]

