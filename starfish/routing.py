from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path
from .consumers import TotalsConsumer

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter([
        re_path(r'^ws/totals/$', TotalsConsumer.as_asgi()),
    ]),
})
