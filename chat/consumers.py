import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from applicase.models import TAApplication
from channels.db import database_sync_to_async
from django.contrib.auth.mixins import LoginRequiredMixin

class ChatConsumer(AsyncWebsocketConsumer, LoginRequiredMixin):

    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        username = self.scope['user'].username
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        first_name = self.scope["user"].first_name
        last_name = self.scope["user"].last_name
        message_dic = {
            'message': message,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,

        }
        print("REC", message)
        await self.save_message(message, self.scope['user'], self.scope['url_route']['kwargs']['room_name'])

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_dic,
            }
        )

    @database_sync_to_async
    def save_message(self, message, author, application_id):
        application = TAApplication.objects.get(pk=application_id)
        message = Message.objects.create(context=message, author=author, application=application)
        print("REC", message)
        message.save()

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = self.scope["user"].username
        first_name = self.scope["user"].first_name
        last_name = self.scope["user"].last_name
        print(first_name, last_name)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'username': username,
            'message': message,
            'first_name': first_name,
            'last_name': last_name,
        }))
