from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from apps.jobs.models import Job
from django.views.generic import ListView, DetailView

class JobKanbanView(TemplateView):
    template_name = "jobs/kanban.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Group jobs by status
        stages = [choice[0] for choice in Job.STATUS_CHOICES]
        ctx["stages"] = [
            {
                "key": stage,
                "label": dict(Job.STATUS_CHOICES)[stage],
                "jobs": Job.objects.filter(status=stage),
            }
            for stage in stages
        ]
        return ctx

@require_POST
def update_job_status(request):
    job_id = request.POST.get("job_id")
    new_stage = request.POST.get("new_stage")
    job = get_object_or_404(Job, pk=job_id)
    if new_stage in dict(Job.STATUS_CHOICES):
        job.status = new_stage
        job.save()
        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False}, status=400)

class JobListView(ListView):
    model = Job
    template_name = "customers/job_list.html"   # you�ll create this

class JobDetailView(DetailView):
    model = Job
    template_name = "customers/job_detail.html" # and this
    context_object_name = "job"
