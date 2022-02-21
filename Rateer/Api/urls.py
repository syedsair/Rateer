from django.urls import path
from .views import api_authenticate, api_creategroup, api_joingroup, api_listgroups, api_listspecifiedgroups, api_createpost, api_groupposts
app_name = "Api"
urlpatterns = [
    path('authenticate', api_authenticate, name="AuthenticateView"),
    path('creategroup', api_creategroup, name="CreateGroupView"),
    path('joingroup', api_joingroup, name="JoinGroupView"),
    path('listgroups', api_listgroups, name="ListGroupsView"),
    path('listspecifiedgroups', api_listspecifiedgroups, name="ListSpecifiedGroupsView"),
    path('createpost', api_createpost, name="CreatePostView"),
    path('grouposts', api_groupposts, name="GroupPostsView"),

]
