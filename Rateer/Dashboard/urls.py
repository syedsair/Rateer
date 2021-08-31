from django.urls import path
from .views import DashboardView, LogoutView, AddEducationView, DelEducationView, AddHobby, DelHobby, EditIntro
app_name = "Dashboard"
urlpatterns = [
    path('', DashboardView, name="DashboardView"),
    path('addeducation/', AddEducationView, name="AddEducationView"),
    path('deleducation/', DelEducationView, name="DelEducationView"),
    path('addhobby/', AddHobby, name="AddHobby"),
    path('delhobby/', DelHobby, name="DelHobby"),
    path('editintro/', EditIntro, name="EditIntro"),
    path('logout/', LogoutView, name="LogoutView"),
]
