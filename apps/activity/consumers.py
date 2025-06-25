# apps/activity/consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ActivityConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        cid = self.scope["url_route"]["kwargs"]["contact_id"]
        self.group = f"activity_{cid}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def new_activity(self, event):
        await self.send_json(event["data"])
