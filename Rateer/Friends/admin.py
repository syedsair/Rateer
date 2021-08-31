from django.contrib import admin
from .models import Friendship, FriendRequests
# Register your models here.
admin.site.register(Friendship)
admin.site.register(FriendRequests)
