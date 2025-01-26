# filepath: /home/abdissad/aait AI 4th +/5yr_1sem/NLP/Threatening_Speech_Detection/threat_detection/threat_detection/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from django.core.asgi import get_asgi_application
from detector.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),
})