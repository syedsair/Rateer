from django.urls import path
from .views import MessengerView, ChatView, DelChat, MSGSaveView, CheckView
app_name = "Messenger"
urlpatterns = [
    path('', MessengerView, name="MessengerView"),
    path('chat/messageCommit/', MSGSaveView, name="MSGSaveView"),
    path('chat/checkNewMessages/', CheckView, name="CheckView"),
    path('chat/<str:username>/', ChatView, name="ChatView"),
    path('delete/<str:username>', DelChat, name="DelChat")
]
