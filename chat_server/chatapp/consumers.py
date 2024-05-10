from django.utils import timezone
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chatapp.models import Message, User
from chatapp.serializers import MessageSerializer, UserSerializer
from schema.global_schema import MessageSchema

import logging
logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("here")
        self.room_name = "chat"
        self.room_group_name = f"group_{self.room_name}"

        # Add user to room members cache (optional)
        user_id = self.scope['user']['id']  # Assume user ID is available from the scope
        if not user_id:
            logger.error("No user_id in scope")
            return
        # cache.set(f'user_{user_id}', timeout=3600)  # Optional user info cache

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        print("here2")
        await self.accept()
        print("here3")
        logger.info(f"Connect new user to conversation with user_id: {user_id}")

    async def disconnect(self, user_id):
        # Remove user from room members cache (optional)
        # await cache.delete(f'user_{user_id}')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("closed connection")
        await self.close()
        logger.info(f"Connect new user to conversation with user_id: {user_id}")

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        try:
            date_now = timezone.now()

            # parse the json data into dictionary object
            text_data_json = json.loads(text_data)

            # unpack the dictionary into the necessary parts
            message = text_data_json["data"]["text"]
            user = self.scope["user"]

            new_msg = await self.save_message(text=message, date_now=date_now)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                    {
                        "type": "chat_message",
                        "id": new_msg["id"],
                        "user": user,
                        "text": message,
                        "created_at": str(date_now)
                    }
            )
        except KeyError as error:
            logger.error(f"Key error in receive message data doesn't sent accepted type: {error}")
        except Exception as error:
            logger.error(f"Exception in receive message: {error}")

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
        user_id = self.scope['user']['id']
        try:
            logger.info("Saving message")
            message = Message.objects.create(
                user_id=user_id,
                text=text,
                created_at=date_now,
            )
            logger.info(f"Save message by user_id: user_id: {user_id}, crypted_text: {text}")
            return MessageSerializer(instance=message).data
        except Exception as err:
            print("Save Message ERROR: ", err)
            self.disconnect(user_id)