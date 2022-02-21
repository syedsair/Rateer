from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from .models import ApiPerson, ApiGroup, ApiGroupMembers,ApiPost,ApiGroupPosts
import datetime


# Create your views here.
def api_authenticate(request):
    data = {
        'message': "",
        'role': ""
    }
    username = request.GET["username"]
    password = request.GET["password"]

    user = authenticate(username=username, password=password)
    if user:
        data['message'] = "Authenticated"
        login(request, user)
        thisuser = User.objects.get(username=username)
        thisperson = ApiPerson.objects.get(ThisUser=thisuser)

        data['email'] = thisperson.ThisUser.email
        data['name'] = thisperson.Name
        data['role'] = thisperson.Role
        data['age'] = thisperson.Age
        data['status'] = thisperson.Status
        data['address'] = thisperson.Address
        data['phone'] = thisperson.Phone
        data['gender'] = thisperson.Gender

    else:
        data['message'] = "Invalid Credentials!"
    return HttpResponse(json.dumps(data))


def api_creategroup(request):
    group_name = request.GET['group_name']
    group_desc = request.GET['group_desc']
    groups = ApiGroup.objects.filter(Name=group_name)
    if len(groups) == 0:
        group = ApiGroup.objects.create(Name=group_name, Description=group_desc).save()

    else:
        return HttpResponse(json.dumps({'message': 'Group Already Exists!'}))
    return HttpResponse(json.dumps({'message': 'Group Created!'}))


def api_joingroup(request):
    group_name = request.GET['group_name']
    username = request.GET['username']
    data = {}

    group = ApiGroup.objects.get(Name=group_name)
    user = User.objects.get(username=username)

    group_members = ApiGroupMembers.objects.filter(GroupId=group.Name, UserId=user.username)
    if len(group_members) > 0:
        data['message'] = "User Already Exists in Specified Group!"
    else:
        ApiGroupMembers.objects.create(GroupId=group.Name, UserId=user.username).save()
        data['message'] = "User Joined the Specified Group!"

    return HttpResponse(json.dumps(data))


def api_listgroups(request):
    groups = ApiGroup.objects.all()
    data = {
        'groups': []
    }
    lis = []
    for i in range(len(groups)):
        current_group = {
            'Group Name': groups[i].Name,
            'Group Description': groups[i].Description
        }
        lis.append(current_group)
    data['groups'] = lis
    return HttpResponse(json.dumps(data))


def api_listspecifiedgroups(request):
    username = request.GET['username']
    user = User.objects.get(username=username)
    accessible_groups = ApiGroupMembers.objects.filter(UserId=user.username)
    lis = []
    for i in range(len(accessible_groups)):
        lis.append(accessible_groups[i].GroupId)
    data = {
        'groups': lis
    }
    return HttpResponse(json.dumps(data))


def api_createpost(request):
    poster = request.GET['poster']
    caption = request.GET['caption']
    posting_time = datetime.datetime.now()
    image = request.GET['caption']
    group_id = request.GET['group_id']

    ApiPost.objects.create(Poster=poster, Caption=caption,Image=image,PostingTime=posting_time).save()
    post = ApiPost.objects.get(Poster=poster, Caption=caption,Image=image,PostingTime=posting_time)
    ApiGroupPosts.objects.create(GroupId=group_id,PostId=post.PostId)
    return HttpResponse(json.dumps({'message': 'Post Created!'}))


def api_groupposts(request):
    group_id = request.GET['group_id']
    group = ApiGroup.objects.get(Name=group_id)
    group_post = ApiGroupPosts.objects.filter(GroupId=group.Name)

    lis = []
    for i in range(len(group_post)):
        d = {}
        obj = ApiPost.objects.get(PostId=group_post[i].PostId)
        d['Caption'] = obj.Caption
        d['Image'] = str(obj.Image)
        d['PostingTime'] = str(obj.PostingTime)
        d['Poster'] = obj.Poster
        lis.append(d)
    data = {
        'posts': lis
    }
    return HttpResponse(json.dumps(data))