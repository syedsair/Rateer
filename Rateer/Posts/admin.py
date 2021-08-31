from django.contrib import admin
from .models import Posts, Likes, Comments

# Register your models here.
admin.site.register(Posts)
admin.site.register(Likes)
admin.site.register(Comments)