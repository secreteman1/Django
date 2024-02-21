from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Room,Topic
from .forms import RoomForm 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout  
from django.contrib.auth.forms import UserCreationForm   
# rooms = [
#     {'id':1, 'name':'Little something something'},
#     {'id':2, 'name':'Little something something'},
#     {'id':3, 'name':'Little something something'},
# ] 

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
             messages.error(request, "Wrong password")
    context = {'page':page}
    return render(request, 'registration_login.html', context=context)

def registerPage(request):
    
    form = UserCreationForm()
    context = {'form':form}
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'registration_login.html', context=context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(topic__name__icontains=q)
    topics = Topic.objects.all()
    room_count= rooms.count()
    content = {'rooms':rooms, 'topics':topics, 'room_count':room_count}
    return render(request, 'home.html',content)

def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'rooms':room}
    return render(request, 'room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'forms': form}
    return render(request, 'roomform.html', context=context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed to do this')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room )
        if form.is_valid():
            form.save()
            return redirect('home') 
    context = {'forms': form}
    return render(request, 'roomform.html', context=context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed to do this')
    if request.method == 'POST':
        room.delete()
        return redirect('home') 
    return render(request, 'delete.html', {'obj': room})