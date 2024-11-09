from notifications.models import Notification

def get_unread_notifications_user(user):
    unread_notifications = Notification.objects.unread().filter(recipient=user)
    return unread_notifications

def count_notifictions_unread_user(user):
    return get_unread_notifications_user(user).count()