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


class ApiLikes(models.Model):
    LikedPostId = models.ForeignKey(ApiPost, on_delete=models.CASCADE)
    LikerId = models.ForeignKey(user, on_delete=models.DO_NOTHING)


class ApiComments(models.Model):
    PostId = models.ForeignKey(ApiPost, on_delete=models.CASCADE)
    CommentorId = models.ForeignKey(user, on_delete=models.DO_NOTHING)
    Comment = models.CharField(max_length=1024, null=False)
    Time = models.DateTimeField(null=False)


class ApiGroupMembers(models.Model):
    GroupId = models.CharField(max_length=100)
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
    Time = models.DateTimeField()

    def __str__(self):
        return str(self.Complainer) + "-" + str(self.Complain) + "-" + str(self.ComplainStatus)


class ApiMessage(models.Model):
    Sender = models.CharField(max_length=200)
    Receiver = models.CharField(max_length=200)
    Message = models.CharField(max_length=5000, null=False)
    Time = models.DateTimeField(null=False)


class ApiFriendRequests(models.Model):
    Sender = models.ForeignKey(user, on_delete=models.CASCADE, related_name='%(class)s_friend_sender')
    Receiver = models.ForeignKey(user, on_delete=models.DO_NOTHING, related_name='%(class)s_friend_receiver')


class ApiFriendship(models.Model):
    Friend_1 = models.ForeignKey(user, on_delete=models.CASCADE, related_name='%(class)s_friend_first')
    Friend_2 = models.ForeignKey(user, on_delete=models.DO_NOTHING, related_name='%(class)s_friend_second')


class ApiPrivacy(models.Model):
    ThisUser = models.ForeignKey(user, on_delete=models.CASCADE, related_name='%(class)s_friend_first')
    ShowAge = models.BooleanField(default=True)
    ShowEmail = models.BooleanField(default=True)
    ShowGender = models.BooleanField(default=True)
    ShowAddress = models.BooleanField(default=True)
    ShowPhone = models.BooleanField(default=True)
    ShowPosts = models.BooleanField(default=True)


class ApiTimetable(models.Model):
    Dept = models.CharField(max_length=30)
    CourseCode = models.CharField(max_length=10)
    CourseName = models.CharField(max_length=50)
    Day = models.CharField(max_length=8)
    Venue = models.CharField(max_length=15)
    StartsAt = models.CharField(max_length=5)
    EndsAt = models.CharField(max_length=5)


class ApiNotifications(models.Model):
    Receiver = models.CharField(max_length=50)
    Sender = models.CharField(max_length=50)
    Content = models.CharField(max_length=2048)
    Time = models.DateTimeField(null=False)

    def __str__(self):
        return str(self.Sender) + str(self.Content)
