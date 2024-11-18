import json
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import async_to_sync
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache.backends.locmem import _caches as cache


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # self.user = self.scope['user']
        # if self.user == AnonymousUser():
        #     raise DenyConnection("Register before")
        # Join room group
        group_send_dict = {"type": "chat_message", "message": 'joined', 
                           'whom': 'room'}
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name, group_send_dict
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": 'left',
                                   'whom': 'room'}
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        whom = text_data_json["whom"]
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message,
                                  'whom': whom}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        whom = event["whom"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, 'from': 'room'}))
                