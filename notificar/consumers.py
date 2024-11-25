import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from notifications.models import Notification

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send_notifications()

    def disconnect(self, close_code):
        pass

    def send_notifications(self):
        unread_count = Notification.objects.unread().filter(recipient=self.scope['user']).count()
        self.send(text_data=json.dumps({
            'unread_count': unread_count,
        }))
