from django.contrib import admin

# Register your models here.
from chatapp.models import *

admin.site.register(User)
admin.site.register(Message)
admin.site.site_header = 'Chat'
