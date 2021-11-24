from django.urls import path
from . import views
urlpatterns = [
    path('view/friends/',views.view_req,name='user_fr'),
    path('view/friends/remove/<str:username>/',views.remove_from_request,name='remove_user'),
    path('view/friends/add/<str:username>/',views.add_from_request,name='add_user'),
    path('view/user/friends/',views.view_friends,name='VFriends'),
    path('send/request/<str:username>/',views.send_friend_request,name='SendReq'),
    path('view/msgs/<str:username_fr>/',views.view_msgs,name='view_msgs'),
    path('seen/msgs/<str:username>/',views.seen_msgs,name='seen_msgs'),
    path('unseen/msgs/',views.un_seen_msgs,name='seen_msgs'),
    path('user/rooms/',views.get_user_in_room,name='user_rooms')
]