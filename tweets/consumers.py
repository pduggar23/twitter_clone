import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the user from the scope (Authenticated via Token later)
        # For simplicity, we will rely on the frontend sending the user ID in the URL for now
        # Real-world apps use Middleware to decode the Token in headers.
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'notifications_{self.user_id}'

        # Join the user's personal group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from the group (Internal Django Signal)
    async def send_notification(self, event):
        message = event['message']

        # Send message to WebSocket (Frontend)
        await self.send(text_data=json.dumps({
            'message': message
        }))