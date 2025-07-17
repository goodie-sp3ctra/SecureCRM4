# apps/activity/admin.py
from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "event_type", "timestamp")
    list_filter  = ("event_type",)
