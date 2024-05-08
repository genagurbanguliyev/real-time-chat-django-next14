import json

from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from chatapp.models import User
from chatapp.serializers import UserSerializer

@database_sync_to_async
def get_user(id):
    try:
        # user_id = UserSerializer(User.objects.get(pk=id)).data
        # return user_id["id"]
        return UserSerializer(User.objects.get(pk=id)).data
    except Exception as e:
        return AnonymousUser


class MyAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query = dict((x.split('=') for x in scope['query_string'].decode().split('&')))
        user = query.get('user_id')
        print("auth====================== ",user)
        scope['user'] = await get_user(id=user)
        return await super().__call__(scope, receive, send)