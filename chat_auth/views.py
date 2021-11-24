from django.shortcuts import redirect, render
from .forms import SignupForm
from django.contrib.auth.views import auth_login
from django.contrib.auth import logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from chat_main.models import Profile

# Create your views here.

def login (request) :
    if request.method == 'POST':
        email = request.POST['email']
        pas = request.POST['password']
        try :
            getUserEmail = User.objects.get(email=email).username
            user = authenticate(username=getUserEmail,password=pas)
            if user is not None :
                auth_login(request,user)
                return redirect('home')
            else :
                messages.error(request,'Uncorrect Email And Password')
        except :
            messages.error(request,"This Email Doesn't exist in the system ")
    
        return redirect('login')
    return render(request,'auth/login.html')

def signup (request) :
    form = SignupForm()
    if request.method == "POST" :
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user).save()
            auth_login(request,user=user)
            return redirect('home')

    return render(request,'auth/signup.html',{'form':form})

def logout_view (request) :
    logout(request=request)
    return redirect('login')
