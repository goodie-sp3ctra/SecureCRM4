from django.urls import path
from .views import JobKanbanView, update_job_status

app_name = "jobs"

urlpatterns = [
    path("kanban/", JobKanbanView.as_view(), name="kanban"),
    path("kanban/update/", update_job_status, name="kanban_update"),
]
