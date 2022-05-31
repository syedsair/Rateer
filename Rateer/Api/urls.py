from django.urls import path
from .views import (IndexView, api_authenticate, api_creategroup, api_joingroup, api_listgroups,
                    api_listspecifiedgroups, api_createpost, api_groupposts,  api_savecomplain,
                    api_getcomplains, api_deletecomplains, api_signup, api_deactivate_account,
                    api_unarchivegroup, api_archivegroup, api_blockuser, api_unblockuser,
                    api_forget_password, api_sendmessage, api_allchats,api_listusers,api_getspecifieduser,
                    api_getallcomplains, api_respondtocomplain, api_savelike, api_savecomment, api_sendfriendrequest,
                    api_requestresponse, api_deletefriendrequest,api_removefriend,api_leavegroup, api_getprivacy,
                    api_deletepost, api_deletegroup, api_setprivacy, api_chatupdate, api_updatetimetable,
                    api_gettimetable, api_saveunlike, api_getrequests, api_updatepersonalinformation,
                    api_specificuserposts, api_getspecificpost, api_getnotifications, api_resetpassword)
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
    path('respondtocomplain', api_respondtocomplain, name="RespondToComplain"),
    path('savelike', api_savelike, name="SaveLike"),
    path('savecomment', api_savecomment, name="SaveComment"),
    path('sendfriendrequest', api_sendfriendrequest, name="SendFriendRequest"),
    path('requestresponse', api_requestresponse, name="FriendRequestResponse"),
    path('deletefriendrequest', api_deletefriendrequest, name='DeleteFriendRequest'),
    path('removefriend', api_removefriend, name='RemoveFriend'),
    path('leavegroup', api_leavegroup, name='LeaveGroup'),
    path('deletepost', api_deletepost, name='DeletePost'),
    path('deletegroup', api_deletegroup, name="DeleteGroup"),
    path('getprivacy', api_getprivacy, name="GetPrivacy"),
    path('setprivacy', api_setprivacy, name="SetPrivacy"),
    path('chatupdate', api_chatupdate, name="ChatUpdate"),
    path('updatetimetable', api_updatetimetable, name="UpdateTimetable"),
    path('gettimetable', api_gettimetable, name="GetTimetable"),
    path('saveunlike', api_saveunlike, name='SaveUnLike'),
    path('getrequests', api_getrequests, name='GetRequests'),
    path('updatepersonalinfo', api_updatepersonalinformation, name='UpdatePersonalInfo'),
    path('specificuserposts', api_specificuserposts, name='SpecificUserPosts'),
    path('getspecificpost', api_getspecificpost, name="GetSpecificPost"),
    path('getnotifications', api_getnotifications, name="GetNotifications"),
    path('resetpassword', api_resetpassword, name="ResetPassword")
]
