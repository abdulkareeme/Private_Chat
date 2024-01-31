from django.urls import re_path , path
from .consumers import OnlineUsersConsumer

websocket_urlpatterns = [
    path('ws/online-users/' , OnlineUsersConsumer.as_asgi()),
]