import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsuer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chatroom"
        self.group_name = f"chat_{self.room_group_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(
            text_data=json.dumps({"message": message, "username": username})
        )
