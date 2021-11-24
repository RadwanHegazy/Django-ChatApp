from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from chat_main.models import Profile, Message, ChatGroup
from django.db.models import Q
from django.contrib.auth.models import User
# Create your views here.

def view_req (request) :
    getReqeusted = Profile.objects.filter(user=request.user)
    list = []
    for i in getReqeusted:
        for new in i.req.all():
            list.append([new.username,new.profile.image.url])

    return JsonResponse(data=list,safe=False)

def view_friends (request) :
    getReqeusted = Profile.objects.filter(user=request.user)
    list = []
    for i in getReqeusted :
        for new in i.friends.all():
            list.append([new.username,new.profile.image.url,new.profile.is_online,new.profile.msgs.filter(to_user=request.user).count()])
        
    return JsonResponse(data=list,safe=False)


def remove_from_request (request, username) :
    GetUser = User.objects.get(username=username)
    getReqeusted = Profile.objects.filter(user=request.user)
    for i in getReqeusted :
        i.req.remove(GetUser)

    return redirect('home')
    
def add_from_request (request, username) :
    GetUser = User.objects.get(username=username)
    getReqeusted = Profile.objects.filter(user=request.user)
    for i in getReqeusted :
        i.req.remove(GetUser)
        i.friends.add(GetUser)
    x = Profile.objects.get(user=GetUser)
    x.friends.add(request.user)


    return redirect('home')



def send_friend_request (request, username) :
    
    getUser = User.objects.get(username=username)
    prof = Profile.objects.get(user=getUser)
    prof.req.add(request.user)
    if 'q' in request.GET : 
        q = request.GET['q']
        return redirect(f'search/?q={q}')
    else :
        return redirect('search')


def view_msgs (request,username_fr) :
    friend = User.objects.get(username=username_fr)
    user = request.user

    msgs = Message.objects.filter(Q(from_user=user,to_user=friend)|Q(from_user=friend,to_user=user)).values('msg','from_user','img').order_by('date')

    return JsonResponse(data=list(msgs),safe=False)


def seen_msgs (request,username) :
    from_ = request.user
    to_ = User.objects.get(username=username)
    Msgs = Message.objects.filter(from_user=to_)
    Msgs.update(seen=True)
    New_Msgs = Message.objects.filter(Q(from_user=from_,to_user=to_)|Q(from_user=to_,to_user=from_))
    prof = Profile.objects.get(user=from_)
    

    for i in New_Msgs :
        if i in prof.msgs.all():
            if i.seen == False :
                pass
            else :
                prof.msgs.remove(i)
        else:   
            pass

    return JsonResponse(data='Ok !',safe=False)

def un_seen_msgs(request):
    user = request.user
    total_unseen = Message.objects.filter(to_user=user).exclude(seen=True)

    return JsonResponse(data="Done",safe=False)

def get_user_in_room (request) : 
    user = request.user
    get_rooms = ChatGroup.objects.filter(users=user)

    return JsonResponse(data=list(get_rooms.values('name','img')),safe=False)