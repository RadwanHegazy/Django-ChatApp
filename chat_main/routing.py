from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path('connect/',consumers.MyConsumer.as_asgi()),
]
