from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
import datetime
from Home.models import Person
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pytz
from .models import Messages
from Dashboard.models import NotificationStatus
utc=pytz.UTC


# Create your views here.
def MessengerView(request):
    user = request.user
    chats = Messages.objects.filter(Q(Sender=user) | Q(Receiver=user)).order_by('-Time')

    names = []
    messages = []

    for chat in chats:
        if chat.Sender == user:
            if chat.Receiver.username not in names:
                names.append(chat.Receiver.username)
                messages.append(chat.Message)
        elif chat.Receiver == user:
            if chat.Sender.username not in names:
                names.append(chat.Sender.username)
                messages.append(chat.Message)
    status = NotificationStatus.objects.filter(ThisUser=user)[0]
    if status.Messenger:
        status.Messenger = False
        status.save()
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed

    data_dict = {
        'person_name': user.username,
        'names': names,
        'messages': messages,
        'ms': ms,
        'nf': nf,
        'fr': fr

    }
    return render(request, 'Messenger.html', context=data_dict)


def ChatView(request, username):
    user = request.user
    user2 = User.objects.get(username=username)

    person = Person.objects.filter(ThisUser=user)[0]
    person2 = Person.objects.filter(ThisUser=user2)[0]

    messages = Messages.objects.filter(
        Q(Q(Sender=user), Q(Receiver=user2)) | Q(Q(Receiver=user), Q(Sender=user2))).order_by('Time')

    status = NotificationStatus.objects.filter(ThisUser=user)[0]
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed

    data_dict = {
        'person': person,
        'person2': person2,
        'messages': messages,
        'ms': ms,
        'nf': nf,
        'fr': fr
    }
    return render(request, 'Chat.html', context=data_dict)


def DelChat(request, username):
    user = request.user
    friend = User.objects.get(username=username)
    chatList1 = Messages.objects.filter(Sender=user, Receiver=friend)
    if chatList1:
        for message in chatList1:
            message.delete()
    return redirect(request.META['HTTP_REFERER'])


def MSGSaveView(request):
    sender = User.objects.get(username=request.POST.get("sender"))
    message = request.POST.get("message")
    receiver = User.objects.get(username=request.POST.get("receiver"))

    messageObj = Messages.objects.create(Sender=sender, Receiver=receiver, Message=message, Time=datetime.datetime.now())
    messageObj.save()

    status = NotificationStatus.objects.filter(ThisUser=receiver)[0]
    status.Messenger = True
    status.save()

    return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def CheckView(request):

    first = User.objects.get(username=request.POST.get("first"))
    second = User.objects.get(username=request.POST.get("second"))
    lastTime = str(request.POST.get("lastTime"))
    print(lastTime)
    if lastTime == "":
        return HttpResponse("Nothing")
    dateArray = lastTime.split()

    dateTempX = dateArray[0].split('/')
    date = int(dateTempX[0])
    month = int(dateTempX[1])
    year = int(dateTempX[2])

    hour = int(dateArray[1].split(':')[0])
    minutes = int(dateArray[1].split(':')[1])
    seconds = int(dateArray[1].split(':')[2])

    d = datetime.datetime(year, month, date, hour=hour, minute=minutes, second=seconds)
    newMessages = []
    messages = Messages.objects.filter(Sender=second, Receiver=first)
    for message in messages:
        messageDate = datetime.datetime(message.Time.year, message.Time.month, message.Time.day, message.Time.hour,
                                        message.Time.minute, message.Time.second)
        if messageDate > d:
            newMessages.append(message)

    data = {
        'person': Person.objects.get(ThisUser=first),
        'person2': Person.objects.get(ThisUser=second),
        'messages': newMessages
    }
    if newMessages:
        return render(request, 'MoreMessages.html', context=data)
    else:
        return HttpResponse("Nothing")

