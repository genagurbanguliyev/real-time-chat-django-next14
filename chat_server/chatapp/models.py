from django.db import models
from django.utils import timezone
from datetime import datetime
from shortuuid.django_fields import ShortUUIDField


import logging
logger = logging.getLogger(__name__)

class User(models.Model):
    id: str = ShortUUIDField(primary_key=True, length=8, max_length=12)
    name: str = models.CharField(max_length=50, null=True, default='User')
    created_at: datetime = models.DateTimeField(null=False, default=timezone.now())
    updated_at: datetime = models.DateTimeField(null=False, default=timezone.now())

    class Meta:
        ordering = ['-created_at']


class Message(models.Model):
    id: str | int = models.AutoField(primary_key=True)
    user: str = models.ForeignKey(User, to_field="id", on_delete=models.DO_NOTHING, unique=False, null=False, related_name="message")
    text: str = models.TextField(unique=False, null=False)
    created_at: datetime = models.DateTimeField(null=False, default=timezone.now())

    # class Meta:
    #     ordering = ['-created_at']
