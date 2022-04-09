from django.urls import path
from .views import (IndexView, api_authenticate, api_creategroup, api_joingroup, api_listgroups,
                    api_listspecifiedgroups, api_createpost, api_groupposts,  api_savecomplain,
                    api_getcomplains, api_deletecomplains, api_signup, api_deactivate_account,
                    api_unarchivegroup, api_archivegroup, api_blockuser, api_unblockuser,
                    api_forget_password, api_sendmessage, api_allchats,api_listusers,api_getspecifieduser,
                    api_getallcomplains, api_respondtocomplain)
app_name = "Api"
urlpatterns = [
    path('', IndexView, name="IndexView"),
    path('signup', api_signup, name='SignUpView'),
    path('deactivate', api_deactivate_account, name='DeactivateView'),
    path('authenticate', api_authenticate, name="AuthenticateView"),
    path('forgetpassword', api_forget_password, name="ForgetPasswordView"),
    path('creategroup', api_creategroup, name="CreateGroupView"),
    path('archivegroup', api_archivegroup, name="ArchiveGroupView"),
    path('unarchivegroup', api_unarchivegroup, name="UnArchiveGroupView"),
    path('blockuser', api_blockuser, name="BlockUserView"),
    path('unblockuser', api_unblockuser, name="UnblockUserView"),
    path('joingroup', api_joingroup, name="JoinGroupView"),
    path('listgroups', api_listgroups, name="ListGroupsView"),
    path('listspecifiedgroups', api_listspecifiedgroups, name="ListSpecifiedGroupsView"),
    path('createpost', api_createpost, name="CreatePostView"),
    path('grouposts', api_groupposts, name="GroupPostsView"),
    path('savecomplain', api_savecomplain, name="SaveComplain"),
    path('getcomplains', api_getcomplains, name="GetComplains"),
    path('deletecomplain', api_deletecomplains, name="DeleteComplains"),
    path('sendmessage', api_sendmessage, name="SendMessage"),
    path('allchats', api_allchats, name="AllChats"),
    path('listusers', api_listusers, name="ListUsers"),
    path('getspecifieduser', api_getspecifieduser, name="SpecifiedUserView"),
    path('getallcomplains', api_getallcomplains, name="AllComplains"),
    path('respondtocomplain', api_respondtocomplain, name="RespondToComplain")
]
