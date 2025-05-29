"""
ASGI config for starfish project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django
from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application  # Added import

from starfish.consumers import TotalsConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starfish.settings')
django.setup()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter([
        re_path(r'^ws/totals/$', TotalsConsumer.as_asgi()),
    ]),
})
