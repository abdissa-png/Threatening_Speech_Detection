from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('wss/detect/', consumers.AudioConsumer.as_asgi()),
]