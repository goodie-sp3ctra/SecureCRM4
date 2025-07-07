"""
ASGI config for crm_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import apps.activity.routing

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(apps.activity.routing.websocket_urlpatterns)
    ),
    # other protocols (http) fall through to Django’s default
})

from channels.routing import ProtocolTypeRouter, URLRouter
from apps.tasks import routing as task_routing
# … keep existing imports …

application = ProtocolTypeRouter(
    {
        "websocket": URLRouter(task_routing.websocket_urlpatterns),
        "http": get_asgi_application(),  # keep existing HTTP handler
    }
)

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')

application = get_asgi_application()
