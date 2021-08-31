from django.urls import path
from .views import FriendsView, LogoutView, OneFriendView, UnFriendView, RateView, SearchView, FindView, RequestView, IncomingRequestsView, AcceptView
from .views import RejectView
app_name = "Friends"
urlpatterns = [
    path('', FriendsView, name="FriendsView"),
    path('search/', SearchView, name="SearchView"),
    path('accept/<str:name>', AcceptView, name="AcceptView"),
    path('reject/<str:name>', RejectView, name="RejectView"),
    path('requests/', IncomingRequestsView, name="IncomingRequestsView"),
    path('friendrequest/<str:friend>/', RequestView, name="RequestView"),

    path('unfriend/<str:username>/', UnFriendView, name="UnFriendView"),
    path('rate/<str:username>/<int:rating>/', RateView, name="RateView"),

    path('find/', FindView, name="FindView"),
    path('logout/', LogoutView, name="LogoutView"),
    path('<str:username>/', OneFriendView, name="OneFriendView"),
]
