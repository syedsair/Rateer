from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Messages(models.Model):
    Sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='%(class)s_sender_person')
    Receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='%(class)s_receiver_person')
    Message = models.CharField(max_length=5000, null=False)
    Time = models.DateTimeField(null=False)