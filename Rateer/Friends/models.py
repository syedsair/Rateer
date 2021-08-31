from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Friendship(models.Model):
    Friend_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_friend_first')
    Friend_2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='%(class)s_friend_second')


class FriendRequests(models.Model):
    Sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_friend_sender')
    Receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='%(class)s_friend_receiver')