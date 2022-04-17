from django.shortcuts import render
from .models import Message
from django.db.models import Q

def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    messages = Message.objects.filter(application_id=int(room_name))
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages,
        'user': request.user,
    })