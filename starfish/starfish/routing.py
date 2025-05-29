from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from starfish.consumers import TotalsConsumer
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'^ws/totals/$', TotalsConsumer.as_asgi()),
        ])
    ),
})
