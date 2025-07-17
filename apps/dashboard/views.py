# apps/dashboard/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.db.models import Count
from django.shortcuts      import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.db.models      import Count
from django.utils.timezone import now

from apps.customers.models      import Job      # ← FIXED!
from apps.customers.models import Client

@login_required
def customer_list(request):
    """Customers page accessible only to authenticated users."""
    # In a real app, you might fetch customer objects here to display.
    return render(request, 'dashboard/customer_list.html')

class DashboardView(TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Summary metrics
        ctx["metrics"] = [
            {"title": "Clients Created", "value": Client.objects.filter(created_at__month=now().month).count()},
            {"title": "Pipelines Won",       "value": Job.objects.filter(status="CLOSED").count()},
            {"title": "Pipelines Lost",      "value": Job.objects.filter(status="CANCELED").count()},
            {"title": "Tasks Closed",        "value": 0},  # fill as you add tasks
            {"title": "Calls Completed",     "value": 0},
            {"title": "Events Completed",    "value": 0},
        ]
        # Chart data
        stages = Job.objects.values("status").annotate(count=Count("id"))
        ctx["chart"] = {
            "labels": [s["status"] for s in stages],
            "values": [s["count"]  for s in stages],
        }
        return ctx