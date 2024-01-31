import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chat.settings')

django.setup()

from conversation.routing import websocket_urlpatterns as conv_urls
from core.routing import websocket_urlpatterns as core_urls
from channels.security.websocket import AllowedHostsOriginValidator
from .middlewares import TokenAuthMiddleware



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(URLRouter(conv_urls+core_urls))
        ),

})
