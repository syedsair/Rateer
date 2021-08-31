from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Posts(models.Model):
    PostId = models.AutoField(primary_key=True)
    Poster = models.ForeignKey(User, on_delete=models.CASCADE)
    Content = models.FileField(upload_to='Posts/')
    Caption = models.CharField(max_length=1024, null=True)
    Event = models.CharField(max_length=254, null=False)
    Time = models.DateTimeField(null=False)


class Likes(models.Model):
    LikedPostId = models.ForeignKey(Posts, on_delete=models.CASCADE)
    LikerPid = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Comments(models.Model):
    LikedPostId = models.ForeignKey(Posts, on_delete=models.CASCADE)
    LikerPid = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    Comment = models.CharField(max_length=1024, null= False)
    Time = models.DateTimeField(null=False)