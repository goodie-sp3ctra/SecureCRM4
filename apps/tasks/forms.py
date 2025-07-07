from django import forms
from .models import Task, Reminder

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title", "description",
            "client", "job",
            "priority", "due", "repeat",
            "assigned_to",
        ]
        widgets = {
            # ↓ put “type” inside attrs
            "due": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
        }


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ["task", "notify_at", "channel"]
        widgets = {
            "notify_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
        }