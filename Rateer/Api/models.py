from django.db import models
from django.contrib.auth.models import User as user

# Create your models here.

ComplainStatusChoices = (
        ('1', 'Submitted'),
        ('2', 'Accepted'),
        ('3', 'Rejected')
    )


class ApiPerson(models.Model):
    ThisUser = models.OneToOneField(user, on_delete=models.CASCADE)

    Age = models.IntegerField(blank=True)
    Status = models.CharField(blank=True, max_length=1024)
    Address = models.CharField(blank=True, max_length=1024)
    Phone = models.CharField(blank=True, max_length=254)
    ProfilePicture = models.ImageField(blank=True, upload_to='ProfilePictures/', max_length=1024,
                                       default='ProfilePictures/DefaultDP.jpg')
    Role = models.CharField(max_length=20)
    RawPassword = models.CharField(max_length=300)
    Name = models.CharField(max_length=1024)
    Gender = models.CharField(max_length=10)

    def __str__(self):
        return self.ThisUser.username


class ApiGroup(models.Model):
    GroupId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.CharField(max_length=2048)
    Archived = models.BooleanField(default=False)
    def __str__(self):
        return self.Name


class ApiPost(models.Model):
    PostId = models.AutoField(primary_key=True)
    Caption = models.CharField(max_length=1024)
    Poster = models.CharField(max_length=100)
    PostingTime = models.TimeField()
    Image = models.ImageField(upload_to='Posts/', max_length=1024)

    def __str__(self):
        return self.Caption


class ApiGroupMembers(models.Model):
    GroupId = models.CharField(max_length=100,primary_key=True)
    UserId = models.CharField(max_length=100)


class ApiGroupPosts(models.Model):
    GroupId = models.CharField(max_length=100)
    PostId = models.CharField(max_length=100)


class ApiComplain(models.Model):
    ComplainId = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=512)
    Complain = models.CharField(max_length=2048)
    ComplainStatus = models.CharField(max_length=500, choices=ComplainStatusChoices)
    Complainer = models.CharField(max_length=200)

    def __str__(self):
        return str(self.Complainer) + "-" + str(self.Complain) + "-" + str(self.ComplainStatus)
