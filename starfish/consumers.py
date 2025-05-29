from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .utils import get_the_totals

class TotalsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('totals_group', self.channel_name)
        await self.accept()
        total = get_the_totals()
        await self.send(text_data=json.dumps({'total': total}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('totals_group', self.channel_name)

    async def receive(self, text_data):
        pass

    async def totals_update(self, event):
        message = event['message']
        await self.send(text_data=message)
