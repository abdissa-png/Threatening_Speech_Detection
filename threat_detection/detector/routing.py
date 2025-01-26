from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('detect/', consumers.AudioConsumer.as_asgi()),
]