from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from django.core.asgi import get_asgi_application
from detector.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path('ws/', URLRouter(websocket_urlpatterns))
    ]),
})