from django.db import models
from django.contrib.auth.models import User as user


# Create your models here.
class Person(models.Model):
    ThisUser = models.OneToOneField(user, on_delete=models.CASCADE)

    Age = models.IntegerField(null=True)
    Status = models.CharField(max_length=1024)
    Address = models.CharField(max_length=1024)
    Phone = models.CharField(max_length=254)
    ProfilePicture = models.ImageField(null=True, upload_to='ProfilePictures/', max_length=1024,
                                       default='ProfilePictures/DefaultDP.jpg')
    Profession = models.CharField(max_length=254)

    def __str__(self):
        return self.ThisUser.username


class Feedback(models.Model):
    UserName = models.CharField(max_length=254, null=False)
    Subject = models.CharField(max_length=254, null=False)
    Message = models.CharField(max_length=3000, null=False)


class Privacy(models.Model):
    ThisUser = models.ForeignKey(user ,on_delete=models.CASCADE)
    Email = models.BooleanField(default=True)
    Age = models.BooleanField(default=True)
    Address = models.BooleanField(default=True)
    Phone = models.BooleanField(default=True)
    Profession = models.BooleanField(default=True)
    Educations = models.BooleanField(default=True)
    Hobbies = models.BooleanField(default=True)