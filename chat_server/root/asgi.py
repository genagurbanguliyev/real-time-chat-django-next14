import os
from django.core.asgi import get_asgi_application

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from chatapp.check_auth import MyAuthMiddleware
from chatapp.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":  AllowedHostsOriginValidator(
            MyAuthMiddleware(
                    URLRouter(
                        websocket_urlpatterns
                ),
    ))
})
