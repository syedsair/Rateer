from django.shortcuts import render
from Home.models import Person, Privacy
from .forms import EducationForm, HobbyForm, IntroForm
from .models import Education, Hobbies, Ratings, NotificationStatus
from django.http import HttpResponseRedirect
from django.contrib.auth import logout


# Create your views here.
def EditIntro(request):
    user = request.user
    person = Person.objects.get(ThisUser=user)
    data_dict = {}
    message = ""
    if request.method == 'POST':
        form = IntroForm(request.POST,request.FILES, instance=person)

        if form.is_valid():
            form.save(commit=True)
            data_dict['form'] = form
            message = "Intro Information Updated!"
        else:
            message = " Intro Updation Failed"
    else:
        data_dict['form'] = IntroForm(instance=person)
    status = NotificationStatus.objects.filter(ThisUser=user)[0]
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed
    data_dict['message'] = message
    data_dict['ms'] = ms
    data_dict['nf'] = nf
    data_dict['fr'] = fr
    return render(request, 'EditIntro.html', data_dict)


def DelHobby(request):
    user = request.user
    data_dict = {}
    message = ""
    if request.method == 'POST':
        form = HobbyForm(request.POST, instance=user)

        if form.is_valid():
            hobby_name = form.cleaned_data.get("Hobby")
            hobby_object = Hobbies.objects.filter(Hobby=hobby_name)
            if hobby_object:
                hobby_object.delete()
                message = "Hobby Deleted!"
            else:
                message = "No Such Hobby Found!"

            data_dict['form'] = form
        else:
            data_dict['form'] = form
            message = " Hobby Deletion Failed"
    else:
        data_dict['form'] = HobbyForm()
    status = NotificationStatus.objects.filter(ThisUser=user)[0]
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed
    data_dict['message'] = message
    data_dict['ms'] = ms
    data_dict['nf'] = nf
    data_dict['fr'] = fr
    return render(request, 'EditIntro.html', data_dict)


def DashboardView(request):
    user = request.user
    person = Person.objects.get(ThisUser=user)
    hobbies = Hobbies.objects.filter(ThisUser=user)
    educations = Education.objects.filter(ThisUser=user)
    picture = person.ProfilePicture

    sum = 0
    count = 0
    ratings = Ratings.objects.filter(RatedPid=user)
    for rating in ratings:
        sum += rating.Rating
        count += 1

    if count:
        rate = sum/count
    else:
        rate = 0
    rate = round(rate, 2)

    status = NotificationStatus.objects.filter(ThisUser= user)[0]
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed

    data = {
        'person_name': user.username,
        'person_status': person.Status,
        'person_rate': rate,
        'person_email': user.email,
        'person_age': person.Age,
        'person_addr': person.Address,
        'person_num': person.Phone,
        'person_prof': person.Profession,
        'person_pic': picture.url,
        'hobbies': hobbies,
        'educations': educations,
        'ms': ms,
        'nf': nf,
        'fr': fr,
    }
    return render(request, 'Dashboard.html', context=data)


def AddEducationView(request):
    user = request.user
    data_dict = {}
    message = ""
    if request.method == 'POST':
        form = EducationForm(request.POST)

        if form.is_valid() and len(Education.objects.filter(ThisUser=request.user, Degree=request.POST.get("Degree"))) == 0:
            edu = form.save(commit=False)
            edu.ThisUser = user
            edu.save()
            data_dict['form'] = form
            message = "Certification Added!"
        else:
            data_dict['form'] = form
            message = " Certification Addition Failed"
    else:
        data_dict['form'] = EducationForm()
    status = NotificationStatus.objects.filter(ThisUser=user)[0]
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed
    data_dict['message'] = message
    data_dict['ms'] = ms
    data_dict['nf'] = nf
    data_dict['fr'] = fr
    return render(request, 'EditIntro.html', data_dict)


def DelEducationView(request):
    user = request.user
    data_dict = {}
    message = ""
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=user)

        if form.is_valid():
            edu = form.cleaned_data.get("Degree")
            eduObj = Education.objects.filter(Degree=edu)
            if eduObj:
                eduObj.delete()
                message = "Education Deleted!"
            else:
                message = "No Such Education Found!"
            data_dict['form'] = form
    else:
        data_dict['form'] = EducationForm()
    status = NotificationStatus.objects.filter(ThisUser=user)[0]
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed
    data_dict['message'] = message
    data_dict['ms'] = ms
    data_dict['nf'] = nf
    data_dict['fr'] = fr
    return render(request, 'EditIntro.html', data_dict)


def AddHobby(request):
    data_dict = {}
    message = ""
    if request.method == 'POST':
        form = HobbyForm(request.POST)

        if form.is_valid() and len(Hobbies.objects.filter(ThisUser=request.user, Hobby=request.POST.get("Hobby"))) == 0:
            form.save(commit=False)
            hobby = Hobbies.objects.create(ThisUser=request.user, Hobby=request.POST.get("Hobby"))
            hobby.save()
            data_dict['form'] = form
            message = "Hobby Added!"
        else:
            data_dict['form'] = form
            message = " Hobby Addition Failed"
    else:
        data_dict['form'] = HobbyForm()
    status = NotificationStatus.objects.filter(ThisUser=request.user)[0]
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed
    data_dict['message'] = message
    data_dict['ms'] = ms
    data_dict['nf'] = nf
    data_dict['fr'] = fr
    return render(request, 'EditIntro.html', data_dict)


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect('/')


