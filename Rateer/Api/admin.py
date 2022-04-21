from django.contrib import admin
from .models import (ApiPost, ApiPerson, ApiGroup,ApiGroupMembers,ApiGroupPosts,ApiComplain,ApiMessage,
                     ApiLikes,ApiComments, ApiFriendship, ApiFriendRequests, ApiPrivacy, ApiTimetable)

# Register your models here.
admin.site.register(ApiPost)
admin.site.register(ApiPerson)
admin.site.register(ApiGroup)
admin.site.register(ApiGroupMembers)
admin.site.register(ApiGroupPosts)
admin.site.register(ApiComplain)
admin.site.register(ApiMessage)
admin.site.register(ApiLikes)
admin.site.register(ApiComments)
admin.site.register(ApiFriendship)
admin.site.register(ApiFriendRequests)
admin.site.register(ApiPrivacy)
admin.site.register(ApiTimetable)