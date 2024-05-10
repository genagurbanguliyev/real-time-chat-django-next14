import json

from django.utils import timezone
from django.http import Http404, HttpResponseServerError
from rest_framework.exceptions import NotAuthenticated, APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chatapp.models import Message, User
from chatapp.serializers import MessageSerializer, UserSerializer
from schema.global_schema import MessageSchema

import logging
logger = logging.getLogger(__name__)


class CheckUserViewSet(APIView):
    @staticmethod
    def get(request, format=None):
        user_id = request.headers.get('User')

        if user_id is None:
            logger.error('Request Without User id, user_id is None')
            raise NotAuthenticated(detail="user_id is None", code=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=user_id)
            serialized = UserSerializer.serialize(user)
            logger.info(f"Get User info:  {serialized}")
            return Response(status=status.HTTP_200_OK, data=serialized)
        except User.DoesNotExist as err:
            print("============== ", err)
            logger.error(err)
            raise Http404

    @staticmethod
    def post(request, format=None):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"User saved: {serializer.data}")
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            if serializer.errors:
                logger.error(f"User saved: {serializer.data}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            logger.error(f"Internal Server Error: {error}")
            raise APIException


class MessagesViewSet(APIView):

    @staticmethod
    def get(request, format=None):
        user_id = request.headers.get('User')

        if user_id is None:
            logger.error('Request Without User id, user_id is None')
            raise NotAuthenticated(detail="user_id is None", code=status.HTTP_403_FORBIDDEN)
        logger.debug(f"try to get user By user_id:  {user_id}")

        try:
            messages: MessageSchema = MessageSerializer(Message.objects.all(), many=True).data
            logger.info("Got messages")
            return Response(status=status.HTTP_200_OK, data=messages)
        except User.DoesNotExist as err:
            print("============== ", err)
            logger.error(err)
            raise Http404


class MessagesLongPollingViewSet(APIView):
    @staticmethod
    def get(request, format=None):
        last_message_id = request.GET.get('last_message_id', None)
        logger.info(f"MessagesLongPollingViewSet with last_message_id: {last_message_id}")
        timeout: int = 5  # Timeout in seconds
        messages: MessageSchema | None = None
        # Filter messages that are newer than the last message the client has
        if last_message_id:
            messages = Message.objects.filter(id__gt=last_message_id)
            logger.info(f"MessagesLongPollingViewSet messages: {MessageSerializer(messages, many=True).data}")

        # If there are new messages, return them immediately
        if messages.exists():
            serializer = MessageSerializer(messages, many=True)
            logger.info(f"MessagesLongPollingViewSet with messages: {serializer.data}")
            return Response(serializer.data)

        # If there are no new messages, wait for a specified timeout
        # This is a simplified example. In a production environment, you might want to use a more efficient waiting mechanism
        import time
        time.sleep(timeout)

        # Check again for new messages after the timeout
        if last_message_id:
            messages = Message.objects.filter(id__gt=last_message_id)
        # else:
        #     messages = []

        if messages.exists():
            serializer = MessageSerializer(messages, many=True)
            logger.info(f"MessagesLongPollingViewSet with messages: {serializer.data}")
            return Response(serializer.data)
        else:
            logger.info(f"MessagesLongPollingViewSet: No new messages")
            return Response(status=status.HTTP_204_NO_CONTENT, data=messages)

    @staticmethod
    def post(request, format=None):
        user_id = request.headers.get('User')
        data = request.data
        date_now = timezone.now()
        print("LongPulling Post Data: ", data)
        logger.info(f"LongPulling Post Data: {data}")
        try:
            logger.info("Saving message")
            message = Message.objects.create(
                user_id=user_id,
                text=data["data"]["text"],
                created_at=date_now,
            )
            logger.info(f"Long Polling = Save message by user_id: {user_id}, crypted_text: {data["data"]["text"]}")
            return Response(MessageSerializer(instance=message).data)
        except Exception as err:
            error_message = "An internal server error occurred: " + str(err)
            print("Save Message ERROR with str: ", error_message)
            print("Save Message ERROR without: ", err)
            return HttpResponseServerError(error_message)

# class ExampleViewSet(APIView):
#     def get_object(self, pk):
#         try:
#             return Message.objects.get(pk=pk)
#         except Message.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         msg = self.get_object(pk)
#         serializer = MessageSerializer(msg)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         msg = self.get_object(pk)
#         serializer = MessageSerializer(msg, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         msg = self.get_object(pk)
#         msg.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

