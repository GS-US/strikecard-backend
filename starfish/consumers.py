from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .utils import get_the_totals

class TotalsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        total = get_the_totals()
        await self.send(text_data=json.dumps({'total': total}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass
