from django.urls import re_path
from .consumers import ChatConsuer

websocket_urlpattern = [re_path(r"ws/chat/$", ChatConsuer.as_asgi())]
