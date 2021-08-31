from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Education(models.Model):
    ThisUser = models.ForeignKey(User, on_delete=models.CASCADE)
    Degree = models.CharField(max_length=254, null=False)
    Institute = models.CharField(max_length=254, null=True)
    From = models.DateField(null=True)
    Till = models.DateField(null=True)


class Hobbies(models.Model):
    ThisUser = models.ForeignKey(User, on_delete=models.CASCADE)
    Hobby = models.CharField(max_length=254, null=False)


class Ratings(models.Model):
    RatedPid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_rated_person')
    RaterPid = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='%(class)s_rater_person')
    Rating = models.FloatField(null=False)


class NotificationStatus(models.Model):
    ThisUser = models.ForeignKey(User, on_delete=models.CASCADE)
    Messenger = models.BooleanField(default= False)
    Requests = models.BooleanField(default= False)
    Feed = models.BooleanField(default=False)