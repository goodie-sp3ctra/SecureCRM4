# apps/activity/routing.py
from django.urls import re_path
from .consumers import ActivityConsumer

websocket_urlpatterns = [
    re_path(r"^ws/activity/(?P<contact_id>\d+)/$", ActivityConsumer.as_asgi()),
]
