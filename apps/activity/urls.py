# apps/activity/urls.py
from django.urls import path
from .views import TimelineView

app_name = "activity"

urlpatterns = [
    path("<int:pk>/timeline/", TimelineView.as_view(), name="timeline"),
]
