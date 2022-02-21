from django.contrib import admin
from .models import ApiPost, ApiPerson, ApiGroup,ApiGroupMembers,ApiGroupPosts

# Register your models here.
admin.site.register(ApiPost)
admin.site.register(ApiPerson)
admin.site.register(ApiGroup)
admin.site.register(ApiGroupMembers)
admin.site.register(ApiGroupPosts)