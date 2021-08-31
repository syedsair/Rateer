from django.urls import path
from .views import HomeView, ContactView, AboutView, SignInView, SignUpView, RegisterView, AuthenticateView, SettingsView, PView
app_name = "Home"
urlpatterns = [
    path('', HomeView, name="HomeView"),
    path('contactus/', ContactView, name="ContactView"),
    path('setprivacy/', PView, name='PView'),
    path('settings/', SettingsView, name='SettingsView'),
    path('about/', AboutView, name="AboutView"),
    path('signin/', SignInView, name="SignInView"),
    path('signup/', SignUpView, name="SignUpView"),
    path('signup/register/', RegisterView, name="RegisterView"),
    path('signin/authenticate/', AuthenticateView, name="AuthenticateView"),
]
