from django.contrib import admin
from .models import Ratings, Hobbies, Education, NotificationStatus


# Register your models here.
admin.site.register(Ratings)
admin.site.register(Hobbies)
admin.site.register(Education)
admin.site.register(NotificationStatus)
