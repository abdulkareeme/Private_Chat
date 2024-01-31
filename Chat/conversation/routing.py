from django.urls import re_path , path
from .consumers import ChatConsumer , PrivateNotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/private_chat/(?P<username>\w+)', ChatConsumer.as_asgi()),
    path('ws/notification/' , PrivateNotificationConsumer.as_asgi()),
]