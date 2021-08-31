from django.shortcuts import render
from .forms import UserForm, FeedbackForm
from .models import Person, Privacy
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from Dashboard.models import NotificationStatus
from django.contrib.auth import authenticate, login


# Create your views here.
def HomeView(request):
    users = len(User.objects.filter())
    data = {
        'users': users,
        'ratings': users,
        'connections': users,
    }
    return render(request, 'HomeTemplate.html', context=data)


def ContactView(request):
    message = ""
    if request.method == "POST":
        form = FeedbackForm(data=request.POST)
        form.UserName = request.POST.get("UserName")
        form.Subject = request.POST.get("Subject")
        form.Message = request.POST.get("Message")

        if form.is_valid():
            user = form
            user.save(commit=True)
            message = "Thank you for your review. We're sorry to hear you had such a frustrating experience, " \
                      "but we really appreciate you bringing this issue to our attention. "
        else:
            message = "Could Not Post Feedback!"
    else:
        form = FeedbackForm()
    data = {
        'message': message,
        'form': form,
    }
    return render(request, 'ContactUs.html', context=data)


def AboutView(request):
    return render(request, 'AboutUs.html')


def SignUpView(request):
    return render(request, 'SignUp.html')


def SignInView(request):
    return render(request, 'SignIn.html')


def RegisterView(request):
    # register user here
    message = ""
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        user_form.username = request.POST.get("username")
        user_form.email = request.POST.get("email")
        user_form.password = request.POST.get("password")

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            person = Person(ThisUser=user)
            person.save()

            status = NotificationStatus.objects.create(ThisUser = user)
            status.save()

            p = Privacy.objects.create(ThisUser = user)
            p.save()

            message = "Registered Successfully!"
        else:
            message = "Could Not Register with Provided Credentials!"

    data = {
        'message': message,
    }
    return render(request, 'SignUp.html', context=data)


def AuthenticateView(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            else:
                message = "Account is De Activated!"
        else:
            message = "Invalid Credentials!"
    data = {
        'message': message,
    }
    return render(request, 'SignIn.html', context=data)


def SettingsView(request):
    privacy = Privacy.objects.filter(ThisUser = request.user)
    if privacy:
        privacy = privacy[0]
    else:
        p = Privacy.objects.create(ThisUser=request.user)
        p.save()
        privacy = p
    data = {
        'privacy': privacy,
    }
    return render(request, 'Settings.html', context=data)


def PView(request):
    email = request.POST.get('email')
    age = request.POST.get('age')
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    profession = request.POST.get('profession')
    education = request.POST.get('education')
    hobbies = request.POST.get('hobbies')

    p = Privacy.objects.filter(ThisUser=request.user)[0]

    if email == "checked":
        p.Email = True
    else:
        p.Email = False

    if age == "checked":
        p.Age = True
    else:
        p.Age = False

    if phone == "checked":
        p.Phone = True
    else:
        p.Phone = False

    if address == "checked":
        p.Address = True
    else:
        p.Address = False

    if profession == "checked":
        p.Profession = True
    else:
        p.Profession = False

    if education == "checked":
        p.Educations = True
    else:
        p.Educations = False

    if hobbies == "checked":
        p.Hobbies = True
    else:
        p.Hobbies = False
    p.save()
    data = {
        'privacy': p,
    }
    return render(request, "Settings.html", context=data)

