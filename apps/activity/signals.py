# apps/activity/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from apps.activity.models import Activity
from apps.customers.models import Client

@receiver(pre_save, sender=Client)
def _stash_original(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._original = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            instance._original = None
    else:
        instance._original = None

@receiver(post_save, sender=Client)
def log_client_change(sender, instance, created, raw, **kwargs):
    if raw:
        return

    # --- build the event payload ---
    if created:
        event, note, diffs = "client_created", "New client added", {}
    else:
        event, note = "client_updated", "Client record updated"
        diffs = {}
        orig = getattr(instance, "_original", None)
        if orig:
            for field in instance._meta.fields:
                name = field.name
                before = getattr(orig, name)
                after  = getattr(instance, name)
                if before != after:
                    diffs[name] = {"old": before, "new": after}

    activity = Activity.objects.create(
        contact=instance,
        user=None,               # or pull from threadlocals if you have it
        event_type=event,
        note=note,
        metadata={"changed_fields": diffs},
    )

    # --- broadcast it over Channels ---
    channel_layer = get_channel_layer()
    group_name    = f"activity_{instance.pk}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "new_activity",
            "data": {
                "timestamp": activity.timestamp.isoformat(),
                "event":     activity.event_type,
                "note":      activity.note,
                "metadata":  activity.metadata,
            }
        }
    )


@receiver(post_save, sender=Activity)
def broadcast_new_activity(sender, instance, created, **kwargs):
    # send every save, or guard on created if you prefer
    channel_layer = get_channel_layer()
    group = f"activity_{instance.contact_id}"
    async_to_sync(channel_layer.group_send)(
        group,
        {
          "type": "new_activity",
          "data": {
            "timestamp": instance.timestamp.isoformat(),
            "event": instance.get_event_type_display(),
            "note": instance.note,
          }
        }
    )