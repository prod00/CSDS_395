from django.shortcuts import render, redirect
from .models import Message
from applicase.models import TAPositionChat, TAPositionPost
from django.db.models import Q

def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    messages = Message.objects.filter(position_id=int(room_name))
    ta_position = TAPositionPost.objects.get(pk=room_name)
    ta_chat = TAPositionChat.objects.get(position=ta_position)
    if request.user in ta_chat.members.all():
        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'messages': messages,
            'user': request.user,
        })
    else:
        messages.warning(request, 'You are not a member of this chat!')
        return redirect("home")