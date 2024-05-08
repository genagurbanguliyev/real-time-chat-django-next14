from django.http import Http404
from rest_framework.exceptions import NotAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chatapp.models import Message, User
from chatapp.serializers import MessageSerializer, UserSerializer


class CheckUserViewSet(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        user_id = request.headers.get('User')

        if user_id is None:
            raise NotAuthenticated(detail="user_id is None", code=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=user_id)
            serialized = UserSerializer.serialize(user)
            return Response(status=status.HTTP_200_OK, data=serialized)
        except User.DoesNotExist as err:
            print("============== ", err)
            raise Http404

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessagesViewSet(APIView):
    def get(self, request, format=None):
        user_id = request.headers.get('User')

        if user_id is None:
            raise NotAuthenticated(detail="user_id is None", code=status.HTTP_403_FORBIDDEN)

        try:
            messages = MessageSerializer(Message.objects.all(), many=True).data
            print("-----------------------", messages)
            return Response(status=status.HTTP_200_OK, data=messages)
        except User.DoesNotExist as err:
            print("============== ", err)
            raise Http404

class ExampleViewSet(APIView):
    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        msg = self.get_object(pk)
        serializer = MessageSerializer(msg)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        msg = self.get_object(pk)
        serializer = MessageSerializer(msg, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        msg = self.get_object(pk)
        msg.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

