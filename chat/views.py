from concurrent.futures import thread
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from chat.models import Thread
from django.contrib.auth.models import User , auth
from . models import Thread

def messages_page(request):
    if request.user.is_authenticated:
        threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
        context = {
            'Threads': threads
        }
        return render(request, 'messages.html', context)
    else:
        page = 'login'
        context = {
            'page': page,
        }
        return render(request, 'login3.html',context)    


def user_login(request):
    if request.user.is_authenticated:
        return redirect('messages_page')

    else:    
        page = 'login'
        context = {
            'page': page,
        }
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('messages_page')
            else:
                return render(request, 'login3.html',context)
        else:           
            return render(request, 'login3.html',context)

def user_register(request):
    if request.user.is_authenticated:
        return redirect('messages_page')

    else:  
        page = 'register'
        context = {
            'page':page,
        }
        if request.method == 'POST':
            first_name = request.POST['fisrt_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            user = User.objects.create_user(first_name=first_name,last_name= last_name,username=username,email=email,password=password1)
            user.save()
            login(request,user)

            extusers = User.objects.all()
            for extuser in extusers:
                thread = Thread.objects.create(first_person=extuser,second_person=user)
                thread.save()
            return redirect('messages_page')
        else:
            return render(request, 'login3.html',context)
      


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    page = 'login'
    context = {
            'page': page,
        }
    return render(request, 'login3.html',context)     

