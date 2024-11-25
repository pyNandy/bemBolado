import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import loja.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loja.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            loja.routing.websocket_urlpatterns
        )
    ),
})

