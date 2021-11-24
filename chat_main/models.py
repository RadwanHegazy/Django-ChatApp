from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.



class Message (models.Model) :
    from_user = models.ForeignKey(User,related_name='msgFromUser',on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,related_name='msgToUser',on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    msg = models.CharField(max_length=1000,null=True,blank=True)
    img = models.ImageField(upload_to='static/chat-images/',null=True,blank=True)
    seen = models.BooleanField(default=False)

    def __str__(self) :
        return f"{self.from_user} -> {self.to_user}"




class ChatGroup (models.Model) : 
    admin = models.ForeignKey(User,related_name='user_creation',on_delete=models.CASCADE)
    admins = models.ManyToManyField(User,related_name='admins',blank=True)
    users = models.ManyToManyField(User,related_name='usersIn',blank=True)
    name = models.CharField(max_length=70,unique=False)
    img = models.ImageField(upload_to='static/rooms-images/',default="static/rooms-images/def.svg")

    def __str__(self) :
        return f"{self.name}"

    def CreateRoomAsAdmin(room_admin,room_name) :
        room = ChatGroup.objects.create(admin=room_admin,name=room_name)
        room.save()
        g_room = ChatGroup.objects.get(name=room_name)
        g_room.admins.add(room_admin)
        g_room.users.add(room_admin)


    def AddAdmins (room_admin,room_user,room_name):
        try : 
            get_room = ChatGroup.objects.get(name=room_name)
            if room_admin in get_room.admins.all() :
                get_room.admins.add(room_user)
                get_room.save()
        except Exception as error :
            return f"{error}"

    def RemoveAdmins (room_admin,room_user,room_name):
        try : 
            get_room = ChatGroup.objects.get(name=room_name)
            if room_admin in get_room.admins.all() :
                get_room.admins.remove(room_user)
                get_room.save()
        except Exception as error :
            return f"{error}"

class MsgsRoom (models.Model) :
    from_user = models.ForeignKey(User,related_name='user_msg_room',on_delete=models.CASCADE)
    to_room = models.ManyToManyField(ChatGroup,related_name='group_msgs',blank=True)
    msg = models.CharField(max_length=1000,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to='static/rooms-chat-images/',blank=True)

    def SendMsg (user,msg,room_name) :
        get_room = ChatGroup.objects.get(name=room_name)
        msg = MsgsRoom.objects.create(from_user=user,msg=msg)
        msg.to_room.add(get_room)
        msg.save()



    def __str__(self) :
        return f"{self.from_user}"  



class Profile (models.Model) :
    user = models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    bio = models.CharField(max_length=1000,blank=True,default="")
    image = models.ImageField(upload_to='static/profiles-images/',blank=True,null=True,default='static/profiles-images/default.svg')
    is_online = models.BooleanField(default=False)
    friends = models.ManyToManyField(User,related_name='userFriends',blank=True)
    req = models.ManyToManyField(User,related_name='reqFriends',blank=True)
    msgs = models.ManyToManyField(Message,related_name='msgs',blank=True)


    def __str__(self) :
        return str(self.user)
    
