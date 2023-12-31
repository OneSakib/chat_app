import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"
        # self.room_group_name = f"chat_broadcast"
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name)
        await self.accept()
        # Send  message to the room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "handle_chat_message", "message": "You are connected to WebSocket Successfully!"})

    async def disconnect(self, code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send  message to the room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "handle_chat_message", "message": message})
        # self.send(text_data=json.dumps({"message": message}))

    # Receive message from the room group
    async def handle_chat_message(self, event):
        message = event['message']

        # send message to the websocket
        await self.send(text_data=json.dumps({"message": message}))
