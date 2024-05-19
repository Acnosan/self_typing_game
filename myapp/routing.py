# myapp/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/typing/', consumers.TypingConsumer.as_asgi()),
]
