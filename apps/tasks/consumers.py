from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

class TaskConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user is None or isinstance(user, AnonymousUser):
            await self.close()
            return

        self.group_name = f"tasks_user_{user.pk}"
        await self.channel_layer.group_add(self.group_name,
                                           self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name,
                                               self.channel_name)

    # called by group_send from Celery
    async def new_reminder(self, event):
        await self.send_json(event)