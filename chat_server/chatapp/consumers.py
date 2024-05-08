from django.utils import timezone
import json

from asgiref.sync import sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from chatapp.models import Message, User
from chatapp.serializers import MessageSerializer, UserSerializer
from schema.global_schema import MessageSchema


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("here")
        self.room_name = "chat"
        self.room_group_name = f"group_{self.room_name}"

        # Add user to room members cache (optional)
        user_id = self.scope['user']['id']  # Assume user ID is available from the scope
        # print("============================ ", await self.scope['user'])
        if not user_id:
            return
        # cache.set(f'user_{user_id}', timeout=3600)  # Optional user info cache

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        # messages = MessageSerializer(Message.objects.all(), many=True).data
        # print("============messages================ ",messages)
        # for message in messages:
        #     print("mMMMMMMMMMMMMMMM==== ", message)
        #     print("SENDING MESSAGE TO FUNCTION")
        #     await self.send_message_to_client(message)

        print("here2")
        await self.accept()
        print("here3")

    # @sync_to_async
    # def send_message_to_client(self, message):
    #     print("SENDING MESSAGES TO THE FRONTEND")
    #     self.send(text_data=json.dumps(message))

    async def disconnect(self, user_id):
        # Remove user from room members cache (optional)
        user_id = self.scope['user']['id']  # Assume user ID is available from the scope
        # await cache.delete(f'user_{user_id}')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("closed connection")
        await self.close()
        raise StopConsumer

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        date_now = timezone.now()

        # parse the json data into dictionary object
        text_data_json = json.loads(text_data)
        print("received message:::::::::::::::::: ", text_data_json)

        # unpack the dictionary into the necessary parts
        message = text_data_json["data"]["text"]
        # user = text_data_json["data"]["user"]
        user = self.scope["user"]

        # Send message to room group
        # chat_type = {"type": "chat_message"}
        # res_dict = {**chat_type, **saved_message}
        await self.channel_layer.group_send(
            self.room_group_name,
                {
                    "type": "chat_message",
                    "user": user,
                    "text": message,
                    "created_at": str(date_now)
                }
        )
        await self.save_message(text=message, date_now=date_now)

    async def chat_message(self, event):
        dict_to_be_sent = event.copy()
        dict_to_be_sent.pop("type")

        # Send message to WebSocket
        await self.send(
                text_data=json.dumps(
                    dict_to_be_sent
                )
            )

    @sync_to_async
    def save_message(self, text: str, date_now: any) -> MessageSchema:
        try:
            user_id = self.scope['user']['id']

            message = Message.objects.create(
                user_id=user_id,
                text=text,
                created_at=date_now,
            )
            print("SAVE:+++++++++++++++++++", message)
            print("SAVE:---------------", MessageSerializer(instance=message).data)
            return MessageSerializer(instance=message).data
        except Exception as err:
            print("Save Message ERROR: ", err)
            self.disconnect("user_id")