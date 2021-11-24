from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
urlpatterns = [
    path('',views.home,name='home'),
    path('search/',views.search,name='search'),
    path('edit/profile/',views.edit_profile,name='edit'),
    path('edit/profile/image',views.update_user_profile,name='editImage'),
    # path('change/password/',views.change_password,name='changePas'),
    path('change/password/',PasswordChangeView.as_view(template_name='home/change_password.html'),name='changePas'),
    path('change/password/done',PasswordChangeDoneView.as_view(template_name='home/change_password_done.html'),name='password_change_done'),
    path('<str:username_fr>/',views.chat,name='chat'),
    path('<str:username>/send/',views.send_msg,name='send_msg'),
    path('<str:username>/send/img/',views.send_img,name='send_img'),
    path('create/room/',views.Create_room,name='cr_room'),
    path('room/send/msg/',views.send_msg_from_room,name='msg_room'),
    path('room/<str:roomName>/',views.room,name='room'),
    path('room/view/msgs/<str:roomName>/',views.view_room_msg,name='VroomM'),
    path('room/<str:roomName>/settings/',views.room_settings,name='room_set'),
]