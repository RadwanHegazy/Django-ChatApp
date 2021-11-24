import json
from channels.generic.websocket import WebsocketConsumer
from chat_main.models import Profile
from django.contrib.auth.models import User


class MyConsumer (WebsocketConsumer) :
    def connect(self):
        self.accept()
        self.send('connected to the server !')

    def receive(self, text_data):
        getUser = User.objects.get(id=text_data)
        self.prof = Profile.objects.get(user=getUser)
        self.prof.is_online = True
        self.prof.save() 


    def disconnect(self, code):
        self.prof.is_online = False
        self.prof.save()

     