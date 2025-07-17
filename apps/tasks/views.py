from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView)
from .models import Task
from .forms import TaskForm, ReminderForm

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        qs = super().get_queryset().filter(assigned_to=self.request.user)
        show = self.request.GET.get('show')
        if show == 'completed':
            qs = qs.filter(completed_at__isnull=False)
        elif show == 'overdue':
            qs = qs.filter(completed_at__isnull=True, due__lt=timezone.now())
        return qs


class TaskCreateView(LoginRequiredMixin, CreateView):
    form_class   = TaskForm
    template_name = 'tasks/task_form.html'
    success_url   = reverse_lazy('tasks:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:list")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:list")


# ─────────── REMINDERS ───────────
class ReminderCreateView(LoginRequiredMixin, CreateView):
    form_class = ReminderForm
    template_name = "tasks/reminder_form.html"
    success_url = reverse_lazy("tasks:list")
