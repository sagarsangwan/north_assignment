import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpattern

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "north_assignment.settings")

# application = get_asgi_application()

application = ProtocolTypeRouter(
    {"http": get_asgi_application(), "websocket": URLRouter(websocket_urlpattern)}
)
