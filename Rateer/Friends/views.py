from django.shortcuts import render,redirect
from .models import Friendship, FriendRequests
from Home.models import Person, Privacy
from Dashboard.models import Education, Hobbies, Ratings, NotificationStatus
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import logout


# Create your views here.
def FriendsView(request):
    user = request.user
    friends_list = Friendship.objects.filter(Friend_1=user)

    Friends_list = []
    for i in range(len(friends_list)):
        Friends_list.append(Person.objects.filter(ThisUser=friends_list[i].Friend_2)[0])
    status = NotificationStatus.objects.filter(ThisUser=user)[0]
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed
    data = {
        'friends_list': Friends_list,
        'person_name': user.username,
        'no_of_friends': len(Friends_list),
        'ms': ms,
        'fr': fr,
        'nf': nf
    }
    return render(request, "Friends.html", context=data)


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect('/')


def OneFriendView(request, username):
    user = User.objects.get(username=username)
    person = Person.objects.get(ThisUser=user)
    hobbies = Hobbies.objects.filter(ThisUser=user)
    educations = Education.objects.filter(ThisUser=user)
    picture = person.ProfilePicture

    friends_list1 = Friendship.objects.filter(Friend_1=user, Friend_2= request.user)
    friends_list2 = Friendship.objects.filter(Friend_2=user, Friend_1=request.user)

    req_list1 = FriendRequests.objects.filter(Sender = request.user, Receiver=user)
    req_list2 = FriendRequests.objects.filter(Sender=user, Receiver=request.user)

    f = 0
    if len(friends_list1) > 0 or len(friends_list2) > 0:
        f = 1

    if len(req_list1) > 0:
        f = 2

    if len(req_list2) > 0:
        f = 3

    sum = 0
    count = 0
    ratings = Ratings.objects.filter(RatedPid=user)
    if ratings:
        for rating in ratings:
            sum += rating.Rating
            count += 1

        if count:
            rate = sum / count
        else:
            rate = 0
        rate = round(rate, 2)
    else:
        rate = 0
    status = NotificationStatus.objects.filter(ThisUser=request.user)[0]
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed
    p = Privacy.objects.filter(ThisUser=user)[0]
    data = {
        'person_name': user.username,
        'person_status': person.Status,
        'person_rate': rate,
        'person_age': person.Age,
        'person_addr': person.Address,
        'person_num': person.Phone,
        'person_prof': person.Profession,
        'person_pic': picture.url,
        'hobbies': hobbies,
        'educations': educations,
        'friend': f,
        'ms': ms,
        'fr': fr,
        'nf': nf,
        'privacy': p,
    }
    return render(request, 'FriendProfile.html', context=data)


def UnFriendView(request, username):
    user = request.user
    friend = User.objects.get(username=username)
    Friendship.objects.get(Friend_1=user, Friend_2=friend).delete()
    Friendship.objects.get(Friend_1=friend, Friend_2=user).delete()

    return redirect(request.META['HTTP_REFERER'])


def RateView(request, username, rating):
    user = request.user
    rated = User.objects.get(username=username)
    rateList = Ratings.objects.filter(RatedPid=rated, RaterPid=user)
    if len(rateList) == 0:
        obj = Ratings.objects.create(RatedPid=rated, RaterPid=user, Rating=rating)
        obj.save()
    else:
        obj = rateList[0]
        obj.Rating = rating
        obj.save()
    return redirect(request.META['HTTP_REFERER'])


def SearchView(request):
    status = NotificationStatus.objects.filter(ThisUser=request.user)[0]
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed
    data = {
        'ms': ms,
        'fr': fr,
        'nf': nf
    }
    return render(request, 'FindFriends.html', context=data)

def FindView(request):
    query = str(request.POST.get("queryname"))
    people = Person.objects.filter()
    response_list = []
    for person in people:
        if not str(person.ThisUser.username).lower().find(query.lower()):
            response_list.append(person)
    status = NotificationStatus.objects.filter(ThisUser=request.user)[0]
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed
    data = {
        'response_list': response_list,
        'ms': ms,
        'fr': fr,
        'nf': nf
    }
    return render(request, 'FindFriends.html', context=data)


def RequestView(request, friend):
    sender = request.user
    receiver = User.objects.get(username=friend)
    requestObject = FriendRequests.objects.filter(Sender= sender, Receiver=receiver)

    friends_list1 = Friendship.objects.filter(Friend_1=receiver, Friend_2= request.user)
    friends_list2 = Friendship.objects.filter(Friend_2=receiver, Friend_1=request.user)

    f = 0
    if receiver:
        if len(friends_list1) > 0 or len(friends_list2) > 0:
            f = 1
        else:
            if requestObject:
                f = 2
            else:
                obj = FriendRequests.objects.create(Sender=sender, Receiver=receiver)
                obj.save()
                status = NotificationStatus.objects.filter(ThisUser=receiver)[0]
                status.Requests = True
                status.save()
                f = 2

    hobbies = Hobbies.objects.filter(ThisUser=receiver)
    educations = Education.objects.filter(ThisUser=receiver)
    person = Person.objects.get(ThisUser = receiver)
    picture = person.ProfilePicture
    sum = 0
    count = 0
    ratings = Ratings.objects.filter(RatedPid=receiver)
    if ratings:
        for rating in ratings:
            sum += rating.Rating
            count += 1

        if count:
            rate = sum / count
        else:
            rate = 0
        rate = round(rate, 2)
    else:
        rate = 0
    status = NotificationStatus.objects.filter(ThisUser=request.user)[0]
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed
    p = Privacy.objects.filter(ThisUser=receiver)[0]
    data = {
        'person_name': receiver.username,
        'person_status': person.Status,
        'person_rate': rate,
        'person_age': person.Age,
        'person_addr': person.Address,
        'person_num': person.Phone,
        'person_prof': person.Profession,
        'person_pic': picture.url,
        'hobbies': hobbies,
        'educations': educations,
        'friend': f,
        'ms': ms,
        'fr': fr,
        'nf': nf,
        'privacy': p,
    }
    return render(request, 'FriendProfile.html', context=data)

def IncomingRequestsView(request):
    user = request.user
    requests = FriendRequests.objects.filter(Receiver = user)
    status = NotificationStatus.objects.filter(ThisUser=user)[0]
    if status.Requests:
        status.Requests = False
        status.save()
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed
    data = {
        'person_name': user.username,
        'requests': requests,
        'number': len(requests),
        'ms':ms,
        'nf':nf,
        'fr':fr
    }
    return render(request, 'FriendRequests.html', context=data)

def AcceptView(request, name):
    user2 = User.objects.get(username= name)
    friendObject1 = Friendship.objects.filter(Friend_1 = request.user, Friend_2 = user2)
    friendObject2 = Friendship.objects.filter(Friend_1=user2, Friend_2=request.user)

    if len(friendObject1) <1 and len(friendObject2) <1:
        reqObj = FriendRequests.objects.filter(Receiver=request.user, Sender=user2)
        if len(reqObj) > 0:
            reqObj[0].delete()
        f = Friendship.objects.create(Friend_1 = request.user, Friend_2 = user2)
        f.save()
        f = Friendship.objects.create(Friend_1=user2, Friend_2=request.user)
        f.save()
    user = request.user
    requests = FriendRequests.objects.filter(Receiver=user)
    status = NotificationStatus.objects.filter(ThisUser=user)[0]
    if status.Requests:
        status.Requests = False
        status.save()
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed
    data = {
        'person_name': user.username,
        'requests': requests,
        'number': len(requests),
        'ms': ms,
        'fr': fr,
        'nf': nf
    }
    return render(request, 'FriendRequests.html', context=data)


def RejectView(request, name):
    receiver = request.user
    sender = User.objects.get(username = name)
    object = FriendRequests.objects.filter(Receiver = receiver, Sender = sender)
    if len(object) > 0:
        object[0].delete()
    user = request.user
    requests = FriendRequests.objects.filter(Receiver=user)
    status = NotificationStatus.objects.filter(ThisUser=user)[0]
    if status.Requests:
        status.Requests = False
        status.save()
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed
    data = {
        'person_name': user.username,
        'requests': requests,
        'number': len(requests),
        'ms': ms,
        'fr': fr,
        'nf': nf
    }
    return render(request, 'FriendRequests.html', context=data)