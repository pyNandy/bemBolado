from django.urls import path
from . import views

app_name = 'notificar'

urlpatterns = [
    
    path('listar_notificacao/', views.listar_notificacao, name="listar_notificacao"),
    path('marcar_notificacao_lida/', views.marcar_notificacao_lida, name="marcar_notificacao_lida"),
    path('superuser_notifications/', views.superuser_notifications, name='superuser_notifications'),
    path('unread_notifications_count/', views.unread_notifications_count, name='unread_notifications_count'),
    path('mark_all_as_read/', views.mark_all_as_read, name='mark_all_as_read'),  # Adiciona esta linha
]
