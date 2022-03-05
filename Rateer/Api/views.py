from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from .models import ApiPerson, ApiGroup, ApiGroupMembers,ApiPost,ApiGroupPosts,ApiComplain
import datetime
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


# Create your views here.
def IndexView(request):
    return HttpResponse('Use Api Only!')


def api_signup(request):
    email = request.GET['email']
    name = request.GET['name']
    password = request.GET['password']
    age = request.GET['age']
    status = request.GET['status']
    address = request.GET['address']
    phone = request.GET['phone']
    role = request.GET['role']
    gender = request.GET['age']
    message = ""
    users = User.objects.filter(email=email)
    if len(users) == 0:
        user = User.objects.create_user(name, email, password)
        person = ApiPerson.objects.create(ThisUser=user, Age=age, Status=status, Name=name ,Address=address,RawPassword=password, Phone=phone, Role=role, Gender=gender)
        message = "User Created!"
    else:
        message = "This User Already Exists!"

    return HttpResponse(json.dumps({"message": message}))


def api_authenticate(request):
    data = {
        'message': "",
        'role': ""
    }
    username = request.GET["username"]
    password = request.GET["password"]

    user = authenticate(username=username, password=password)
    if user:
        thisuser = User.objects.get(username=username)
        if thisuser.is_active:
            data['message'] = "Authenticated"
            login(request, user)

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
            message = "User Blocked by Admin!"
    else:
        data['message'] = "Invalid Credentials!"
    return HttpResponse(json.dumps(data))


def api_forget_password(request):
    email = request.GET['email']
    users = User.objects.filter(email=email)
    message = ""
    if len(users) > 0:
        user = users[0]
        if user.is_active:
            person = ApiPerson.objects.get(ThisUser=user)

            email_plaintext_message = "A password reset query has been submitted to FastNet. Password for your account is " + str(person.RawPassword) + "."
            from_email = settings.EMAIL_HOST_USER
            msg = EmailMultiAlternatives(
                "Password Reset For FastNet",
                email_plaintext_message,
                from_email,
                [user.email],
            )
            msg.send()
            message = "Password Sent to User's Email."
        else:
            message = "User Blocked by Admin!"
    else:
        message = "No Such User Exists!"
    return HttpResponse(json.dumps({'message': message}))


def api_deactivate_account(request):
    username = request.GET['username']

    users = User.objects.filter(username=username)
    if len(users) > 0:
        person = ApiPerson.objects.filter(ThisUser=users[0])[0]

        posts = ApiPost.objects.filter(Poster=users[0].username)
        groupPosts = ApiGroupPosts.objects.filter()
        to_be_deleted_group_posts = []
        for i in range(len(posts)):
            for j in range(len(groupPosts)):
                if posts[i].PostId == groupPosts[j].PostId:
                    to_be_deleted_group_posts.append(groupPosts[j])
            posts[i].delete()
        for obj in to_be_deleted_group_posts:
            obj.delete()

        memberships = ApiGroupMembers.objects.filter(UserId=users[0].username)
        for i in range(len(memberships)):
            memberships[i].delete()

        complains = ApiComplain.objects.filter(Complainer=users[0].username)
        for i in range(len(complains)):
            complains[i].delete()

        for i in range(len(memberships)):
            memberships[i].delete()

        person.delete()
        users[0].delete()

        message = "User Deleted!"
    else:
        message = "No Such User Exists"
    return HttpResponse(json.dumps({'message': message}))


def api_archivegroup(request):
    group_id = request.GET['group']
    groups = ApiGroup.objects.filter(Name=group_id)
    if len(groups) > 0:
        groups[0].Archived = True
        groups[0].save(update_fields=['Archived'])
        message = "Group Archived!"
    else:
        message = "No Such Group Exists!"
    return  HttpResponse(json.dumps({'messagee': message}))


def api_unarchivegroup(request):
    group_id = request.GET['group']
    groups = ApiGroup.objects.filter(Name=group_id)
    if len(groups) > 0:
        groups[0].Archived = False
        groups[0].save(update_fields=['Archived'])
        message = "Group Unarchived!"
    else:
        message = "No Such Group Exists!"
    return  HttpResponse(json.dumps({'messagee': message}))


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
    if user.is_active:
        group_members = ApiGroupMembers.objects.filter(GroupId=group.Name, UserId=user.username)
        if len(group_members) > 0:
            data['message'] = "User Already Exists in Specified Group!"
        else:
            ApiGroupMembers.objects.create(GroupId=group.Name, UserId=user.username).save()
            data['message'] = "User Joined the Specified Group!"
    else:
        data['message'] = "User Blocked by Admin!"

    return HttpResponse(json.dumps(data))


def api_listgroups(request):
    groups = ApiGroup.objects.all()
    data = {
        'groups': []
    }
    lis = []
    for i in range(len(groups)):
        if not groups[i].Archived:
            current_group = {
                'Group Name': groups[i].Name,
                'Group Description': groups[i].Description
            }
            lis.append(current_group)
    data['groups'] = lis
    return HttpResponse(json.dumps(data))


def api_blockuser(request):
    user_to_block = request.GET['blockuser']
    users = User.objects.filter(username=user_to_block)
    if len(users) > 0:
        user = users[0]
        user.is_active = False
        user.save(update_fields=['is_active'])
        message = "User Blocked!"
    else:
        message = "No Such User Exists!"
    return HttpResponse(json.dumps({'message': message}))


def api_unblockuser(request):
    user_to_block = request.GET['unblockuser']
    users = User.objects.filter(username=user_to_block)
    if len(users) > 0:
        user = users[0]
        user.is_active = True
        user.save(update_fields=['is_active'])
        message = "User Unblocked!"
    else:
        message = "No Such User Exists!"
    return HttpResponse(json.dumps({'message': message}))


def api_listspecifiedgroups(request):
    username = request.GET['username']
    user = User.objects.get(username=username)
    accessible_groups = ApiGroupMembers.objects.filter(UserId=user.username)
    all_groups = ApiGroup.objects.filter(Archived=False)
    lis = []
    for i in range(len(accessible_groups)):
        for j in range(len(all_groups)):
            if accessible_groups[i].GroupId == all_groups[j].Name:
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
        d['PostId'] = obj.PostId
        d['Caption'] = obj.Caption
        d['Image'] = str(obj.Image)
        d['PostingTime'] = str(obj.PostingTime)
        d['Poster'] = obj.Poster
        lis.append(d)
    data = {
        'posts': lis
    }
    return HttpResponse(json.dumps(data))


def api_deletegroup(request):
    group_id = request.GET['group_id']
    posts = ApiGroupPosts.objects.filter(GroupId=group_id)

    for i in range(len(posts)):
        ApiPost.objects.get(PostId=posts[i].PostId).delete()
        posts[i].delete()

    members = ApiGroupMembers.objects.filter(GroupId=group_id)
    for i in range(len(members)):
        members[i].delete()

    ApiGroup.objects.get(Name=group_id).delete()

    return HttpResponse(json.dumps({'message': 'Group Deleted!'}))


def api_leavegroup(request):
    user = request.GET['username']
    group = request.GET['group_id']
    memberships = ApiGroupMembers.objects.filter(GroupId=group, UserId=user)
    if len(memberships) > 0:
        memberships[0].delete()
        return HttpResponse(json.dumps({'message': 'Group Membership Deleted!'}))
    else:
        return HttpResponse(json.dumps({'message': 'User is not subscribed to this group!'}))


def api_deletepost(request):
    post_id = request.GET['post_id']
    post_groups = ApiGroupPosts.objects.filter(PostId=post_id)
    for i in range(len(post_groups)):
        post_groups[i].delete()

    posts = ApiPost.objects.filter(PostId=post_id)
    for i in range(len(posts)):
        posts[i].delete()

    return HttpResponse(json.dumps({'message': 'Post Deleted!'}))


def api_savecomplain(request):
    message = ''
    try:
        userId = request.GET["username"]
        complain = request.GET["complain"]
        status = "Submitted"
        ApiComplain.objects.create(Complain=complain, Complainer=userId, ComplainStatus=status).save()
        message = 'Complain Recorded!'
    except Exception as e:
        message = 'Please Try Again Later!'
    return HttpResponse(json.dumps({'message': message}))


def api_getcomplains(request):
    user = request.GET['username']
    complainObjects = ApiComplain.objects.filter(Complainer=user)

    complains = []
    for complainObj in complainObjects:
        d = {
            'Complain': complainObj.Complain,
            'Status': complainObj.ComplainStatus
        }
        complains.append(d)
    final_complains = {
        'complains': complains
    }
    return HttpResponse(json.dumps(final_complains))


def api_deletecomplains(request):
    message = ""
    try:
        complainId = request.GET['complainId']
        complains = ApiComplain.objects.filter(ComplainId=complainId)
        if len(complains) > 0:
            complains[0].delete()
            message = 'Complain Removed!'
        else:
            message = 'No Such Complain Exists!'
    except Exception as e:
        message = "Please Try Again Later!"
    return HttpResponse(json.dumps({"message" : message}))
