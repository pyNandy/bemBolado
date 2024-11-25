from django.shortcuts import render, redirect
from django.http import HttpResponse
from notifications.signals import notify
from django.contrib.auth.models import User
from .notifications import get_unread_notifications_user, count_notifictions_unread_user
from notifications.models import Notification
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def listar_notificacao(request):
    unread_notifications = get_unread_notifications_user(request.user)
    count = count_notifictions_unread_user(request.user)  
    return render(request, 'listar_notificacao.html', {'unread_notifications': unread_notifications, 'count': count})

def marcar_notificacao_lida(request):
    Notification.objects.mark_all_as_read(recipient=request.user)
    return redirect(reverse('listar_notificacao'))

@login_required
def superuser_notifications(request):
    if request.user.is_superuser:
        unread_notifications = Notification.objects.unread().filter(recipient=request.user)
        return render(request, 'superuser_notifications.html', {'unread_notifications': unread_notifications})
    else:
        return render(request, 'not_authorized.html')

@login_required
def unread_notifications_count(request):
    if request.user.is_superuser:
        unread_count = Notification.objects.unread().filter(recipient=request.user).count()
        return JsonResponse({'unread_count': unread_count})
    return JsonResponse({'unread_count': 0})

@login_required
def mark_all_as_read(request):
    if request.method == 'POST':
        Notification.objects.filter(recipient=request.user).mark_all_as_read()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

