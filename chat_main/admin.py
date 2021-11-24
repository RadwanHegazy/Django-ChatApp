from django.contrib import admin
from .models import Profile, Message, ChatGroup, MsgsRoom

# Register your models here.
admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(ChatGroup)
admin.site.register(MsgsRoom)