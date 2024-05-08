from django.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField

class User(models.Model):
    # id = models.CharField(primary_key=True, null=False, max_length=200)
    id = ShortUUIDField(primary_key=True, length=8, max_length=12)
    name = models.CharField(max_length=50, null=True, default='User')
    created_at = models.DateTimeField(null=False, default=timezone.now())
    updated_at = models.DateTimeField(null=False, default=timezone.now())

    class Meta:
        ordering = ['-created_at']


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, to_field="id", on_delete=models.DO_NOTHING, unique=False, null=False, related_name="message")
    text = models.TextField(unique=False, null=False)
    created_at = models.DateTimeField(null=False, default=timezone.now())

    # class Meta:
    #     ordering = ['-created_at']
