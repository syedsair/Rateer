from django.contrib import admin
from .models import Person, Feedback, Privacy

# Register your models here.
admin.site.register(Person)
admin.site.register(Privacy)
admin.site.register(Feedback)