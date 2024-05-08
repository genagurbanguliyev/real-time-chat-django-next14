from django.urls import path, re_path
from chatapp import consumers

websocket_urlpatterns = [
    # path('ws/chat/', consumers.ChatConsumer.as_asgi()),
    re_path(r'^ws/chat/$', consumers.ChatConsumer.as_asgi()),
]