from django.db.models.fields import CharField
from chat_json.views import seen_msgs
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import MsgsRoom, Profile
from django.views.generic import UpdateView
from .models import Message, ChatGroup, MsgsRoom
# Create your views here.

def home (request) :
    if request.user.is_authenticated:
        getReqeusted = Profile.objects.filter(user=request.user)
        return render(request,'home/home.html',{'users':getReqeusted})
    else :
        return redirect('login')

def search (request) :
    if 'q' in request.GET :
        q = request.GET['q']
        users = User.objects.filter(username__contains=q).all().exclude(username=request.user.username)
    else :
        users = User.objects.all().exclude(username=request.user.username)
    
    return render(request,'home/search.html',{'users':users})

def edit_profile (request) :
    if request.method == 'POST' :
        username = request.POST['username']
        email = request.POST['email']
        user = User.objects.get(id=request.user.id)
        user.username = username
        user.email = email
        user.save()
        
        if 'bio' in request.POST:
            bio = request.POST['bio']
            print(bio)
            prof = Profile.objects.get(user=user)
            prof.bio = bio
            prof.save()
        
        return redirect('home')


    return render(request,'home/edit_profile.html')

def update_user_profile (request) :
    image = request.FILES['image']
    prof = Profile.objects.get(user=request.user)
    prof.image = image
    prof.save()
    return redirect('edit')


def chat (request,username_fr) :
    friend = get_object_or_404(User,username=username_fr)
    return render(request,'home/chat.html',{'friend':friend})

def send_msg (request,username) :
    to_ = User.objects.get(username=username)
    from_ = request.user
    msg = request.POST['message']

    # save message
    msg = Message.objects.create(from_user=from_,to_user=to_,msg=msg)
    msg.save()

    prof = Profile.objects.get(user=from_)
    
    prof.msgs.add(msg)

    return JsonResponse(data='Done',safe=False)

def send_img (request,username) :
    to_ = User.objects.get(username=username)
    from_ = request.user
    img = request.FILES['image']
    msg = Message.objects.create(from_user=from_,to_user=to_,img=img)
    msg.save()
    prof = Profile.objects.get(user=from_)
    prof.msgs.add(msg)
    # return redirect('chat',username)
    return JsonResponse(data='Done',safe=False)

def Create_room (request) :
    get_fr = Profile.objects.get(user=request.user)
    if request.method == 'POST' :
        users = request.POST.getlist('users')
        name = request.POST['roomName']
        ChatGroup.CreateRoomAsAdmin(room_name=name,room_admin=request.user)
        if users : 
            for i in users :
                get_user = User.objects.get(username=i)
                get_room = ChatGroup.objects.get(name=name)
                get_room.users.add(get_user)
                get_room.save()
        return redirect('home')
    return render(request,'home/create_room.html',{'friends':get_fr.friends.all()})

def send_msg_from_room (request) :
    msg = request.POST['msg']
    room = request.POST['room_name']
    MsgsRoom.SendMsg(user=request.user,room_name=room,msg=msg)
    return JsonResponse(data="Done",safe=False)

def room (request, roomName) :
    room = get_object_or_404(ChatGroup,name=roomName)
    if 'image' in request.FILES: 
        image = request.FILES['image']
        msg = MsgsRoom.objects.create(from_user=request.user,img=image)
        msg.to_room.add(room)
        msg.save()
    return render(request,'home/room.html',{'room':room})


def view_room_msg (request, roomName):
    room = get_object_or_404(ChatGroup,name=roomName)
    room_msgs = MsgsRoom.objects.filter(to_room=room).all().order_by('date')
    return JsonResponse(data=list(room_msgs.values('msg','from_user','img')),safe=False)

def room_settings (request, roomName) :

    room = get_object_or_404(ChatGroup,name=roomName)


    if request.method == "POST" :
        if 'roomName' in request.POST :
            room_name = request.POST['roomName']
            if room.name != room_name : 
                room.name = room_name
                room.save()
          
            users = request.POST.getlist('users')
            admins = request.POST.getlist('admins')
            for i in room.admins.all() :
                try :
                    if i == request.user :
                        pass
                    elif i == room.admin :
                        pass
                    else :
                        room.admins.remove(i)
                except :
                    pass
            
            for i in admins :
                get_user = User.objects.get(username=i)
                room.admins.add(get_user) 

            room = get_object_or_404(ChatGroup,name=room_name)
            for i in room.users.all() :
                try :
                    if i == request.user :
                        pass
                    elif i == room.admin :
                        pass
                    else :
                        room.users.remove(i)
                except :
                    pass
            for us in users: 
                user = User.objects.get(username=us)
                room.users.add(user)

            return redirect('room',room.name)
        elif 'delete' in request.POST :
            room.delete()
            return redirect('home')
        elif 'roomImage' in request.FILES :
            img = request.FILES['roomImage']
            room.img = img
            room.save()
            return redirect('room',room.name)

        else :
            return JsonResponse(request.POST,safe=False)

        
    return render(request,'home/room_options.html',{'room':room})

