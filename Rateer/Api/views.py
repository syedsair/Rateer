from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from .models import ApiPerson,ApiFriendship, ApiFriendRequests, ApiGroup, ApiGroupMembers,ApiPost,ApiGroupPosts,ApiComplain,ApiMessage,ApiLikes,ApiComments
import datetime
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone


# API Key
API_KEY = "5f8641f6-c4e8-490d-b619-2d8bf20d3786"

# Create your views here.
def IndexView(request):
    return HttpResponse('Use Api Only!')


def api_signup(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        email = request.GET['email']
        name = request.GET['name']
        password = request.GET['password']
        age = request.GET['age']
        status = request.GET['status']
        address = request.GET['address']
        phone = request.GET['phone']
        role = request.GET['role']
        gender = request.GET['gender']
        rollno=email.split('@')[0]
        message = ""
        users = User.objects.filter(email=email)
        if len(users) == 0:

            user = User.objects.create_user(rollno, email, password)
            person = ApiPerson.objects.create(ThisUser=user, Age=age, Status=status, Name=name ,Address=address,RawPassword=password, Phone=phone, Role=role, Gender=gender)
            message = "User Created!"
        else:
            message = "This User Already Exists!"

        return HttpResponse(json.dumps({"message": message}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_authenticate(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        data = {
            'message': "",
            'role': ""
        }
        email = request.GET["email"]
        password = request.GET["password"]

        all_users = User.objects.filter()
        final_user = ""
        final_person = ""
        for user in all_users:

            if user.email == email:
                final_user = user
                final_person = ApiPerson.objects.get(ThisUser=final_user)
                if final_person.RawPassword == password:
                    break
                else:
                    final_person = ""
                    final_user = ""

        if final_user != "":
            if final_user.is_active:
                data['message'] = "Authenticated"
                login(request, final_user)
                data['email'] = final_person.ThisUser.email
                data['name'] = final_person.Name
                data['role'] = final_person.Role
                data['age'] = final_person.Age
                data['status'] = final_person.Status
                data['address'] = final_person.Address
                data['phone'] = final_person.Phone
                data['gender'] = final_person.Gender
            else:
                message = "User Blocked by Admin!"
        else:
            data['message'] = "Invalid Credentials!"
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse(json.dumps({"message": 'Invalid Api Key!'}))


def api_forget_password(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
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
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_deactivate_account(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
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
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_archivegroup(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        group_id = request.GET['group']
        groups = ApiGroup.objects.filter(Name=group_id)
        if len(groups) > 0:
            groups[0].Archived = True
            groups[0].save(update_fields=['Archived'])
            message = "Group Archived!"
        else:
            message = "No Such Group Exists!"
        return  HttpResponse(json.dumps({'messagee': message}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_unarchivegroup(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        group_id = request.GET['group']
        groups = ApiGroup.objects.filter(Name=group_id)
        if len(groups) > 0:
            groups[0].Archived = False
            groups[0].save(update_fields=['Archived'])
            message = "Group Unarchived!"
        else:
            message = "No Such Group Exists!"
        return  HttpResponse(json.dumps({'messagee': message}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_creategroup(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        group_name = request.GET['group_name']
        group_desc = request.GET['group_desc']
        groups = ApiGroup.objects.filter(Name=group_name)
        if len(groups) == 0:
            group = ApiGroup.objects.create(Name=group_name, Description=group_desc).save()
        else:
            return HttpResponse(json.dumps({'message': 'Group Already Exists!'}))
        return HttpResponse(json.dumps({'message': 'Group Created!'}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_joingroup(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
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
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_listgroups(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        groups = ApiGroup.objects.all()
        data = {
            'groups': []
        }
        lis = []
        for i in range(len(groups)):
            current_group = {
                'Group Name': groups[i].Name,
                'Group Description': groups[i].Description,
                'Archived Status' : groups[i].Archived
            }
            lis.append(current_group)
        data['groups'] = lis
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_blockuser(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
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
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_unblockuser(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
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
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_listspecifiedgroups(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
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
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_createpost(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        poster = request.GET['poster']
        caption = request.GET['caption']
        posting_time = datetime.datetime.now()
        image = request.GET['caption']
        group_id = request.GET['group_id']

        ApiPost.objects.create(Poster=poster, Caption=caption,Image=image,PostingTime=posting_time).save()
        post = ApiPost.objects.get(Poster=poster, Caption=caption,Image=image,PostingTime=posting_time)
        ApiGroupPosts.objects.create(GroupId=group_id,PostId=post.PostId)
        return HttpResponse(json.dumps({'message': 'Post Created!'}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_groupposts(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
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
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_deletegroup(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
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
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_leavegroup(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        user = request.GET['username']
        group = request.GET['group_id']
        memberships = ApiGroupMembers.objects.filter(GroupId=group, UserId=user)
        if len(memberships) > 0:
            memberships[0].delete()
            return HttpResponse(json.dumps({'message': 'Group Membership Deleted!'}))
        else:
            return HttpResponse(json.dumps({'message': 'User is not subscribed to this group!'}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_deletepost(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        post_id = request.GET['post_id']
        post_groups = ApiGroupPosts.objects.filter(PostId=post_id)
        for i in range(len(post_groups)):
            post_groups[i].delete()

        posts = ApiPost.objects.filter(PostId=post_id)
        for i in range(len(posts)):
            posts[i].delete()

        return HttpResponse(json.dumps({'message': 'Post Deleted!'}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_savecomplain(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        message = ''
        try:
            posting_time = datetime.datetime.now()
            userId = request.GET["username"]
            complain = request.GET["complain"]
            title = request.GET['title']
            status = "Submitted"
            ApiComplain.objects.create(Complain=complain, Complainer=userId, Title=title, ComplainStatus=status,Time=posting_time).save()
            message = 'Complain Recorded!'
        except Exception as e:
            message = 'Please Try Again Later!'
        return HttpResponse(json.dumps({'message': message}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_getcomplains(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        user = request.GET['username']
        complainObjects = ApiComplain.objects.filter(Complainer=user)

        complains = []
        for complainObj in complainObjects:
            d = {
                'complainid': complainObj.ComplainId,
                'title': complainObj.Title,
                'complain': complainObj.Complain,
                'complainstatus': complainObj.ComplainStatus,
                'Time': str(complainObj.Time)
            }
            complains.append(d)
        final_complains = {
            'complains': complains
        }
        return HttpResponse(json.dumps(final_complains))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_deletecomplains(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
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
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_sendmessage(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        message = request.GET['message']
        sender_email = request.GET['sender']
        receiver_email = request.GET['receiver']

        all_users = User.objects.all()
        final_sender_user = ""
        final_receiver_user = ""
        for user in all_users:
            if user.email == sender_email:
                final_sender_user = user
            if user.email == receiver_email:
                final_receiver_user = user
        if final_receiver_user != "" and final_sender_user != "":
            return_message = ""
            try:
                ApiMessage.objects.create(Sender=final_sender_user.username, Receiver=final_receiver_user.username, Message=message, Time=timezone.now()).save()
                return_message = "Message Sent!"
            except Exception as e:
                return_message = "Please Try Again Later!"
        else:
            return_message = "Invalid Input!"

        return HttpResponse(json.dumps({'message': return_message}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_allchats(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        username = request.GET['username']
        sender_messages = ApiMessage.objects.filter(Sender=username)
        receiver_messages = ApiMessage.objects.filter(Receiver=username)
        final_response = []
        sender_email=""
        receiver_email=""
        for message in sender_messages:
            sender_=User.objects.filter(username=message.Sender)
            for s in sender_:
                sender_email=s.email
            receiver_ = User.objects.filter(username=message.Receiver)
            for r in receiver_:
                receiver_email = r.email
            final_response.append({
                'Sender': message.Sender,
                'SenderEmail': sender_email,
                'Receiver': message.Receiver,
                'ReceiverEmail': receiver_email,
                'Message': message.Message,
                'Time': str(message.Time)
            })
        for message in receiver_messages:
            sender_ = User.objects.filter(username=message.Sender)
            for s in sender_:
                sender_email = s.email
            receiver_ = User.objects.filter(username=message.Receiver)
            for r in receiver_:
                receiver_email = r.email
            final_response.append({
                'Sender': message.Sender,
                'SenderEmail': sender_email,
                'Receiver': message.Receiver,
                'ReceiverEmail': receiver_email,
                'Message': message.Message,
                'Time': str(message.Time)
            })
        return HttpResponse(json.dumps({'message': final_response}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_listusers(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        lst=[]
        users=User.objects.filter()
        for u in users:
            final_user = u
            name_ = ApiPerson.objects.filter(ThisUser=final_user)
            if(len(name_)!=0):
                name = name_[0].Name
                data = {
                    'name': name,
                    'email': u.email
                }
                lst.append(data)

        return HttpResponse(json.dumps({"users" : lst}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_getspecifieduser(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        data = {}
        email = request.GET["email"]
        all_users = User.objects.filter(email=email)
        final_user = ""
        final_person = ""
        if len(all_users) != 0:
            data['message'] = "User found!"
            for final_user in all_users:
                final_person = ApiPerson.objects.get(ThisUser=final_user)

            data['email'] = final_person.ThisUser.email
            data['name'] = final_person.Name
            data['role'] = final_person.Role
            data['age'] = final_person.Age
            data['status'] = final_person.Status
            data['address'] = final_person.Address
            data['phone'] = final_person.Phone
            data['gender'] = final_person.Gender
            data['isunblocked']=final_user.is_active

        else:
            data['message'] = "No User by this email"
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_getallcomplains(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        lst=[]
        all_complains = ApiComplain.objects.all()
        if len(all_complains)>0:
            #data['message']="Complains Found!"
            for c in all_complains:
                data = {}
                data['complainid'] = c.ComplainId
                data['title'] = c.Title
                data['complain'] = c.Complain
                data['complainstatus'] = c.ComplainStatus
                data['complainer'] = c.Complainer
                data['Time']= str(c.Time)
                lst.append(data)

        return HttpResponse(json.dumps(lst))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_respondtocomplain(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        complainid=request.GET['complainid']
        response=request.GET['response']
        all_complains=ApiComplain.objects.filter(ComplainId=complainid)
        message=''
        if len(all_complains)>0:
            all_complains[0].ComplainStatus=response
            all_complains[0].save(update_fields=['ComplainStatus'])
            message='Done'
        else:
            message='Invalid Complain ID'
        return HttpResponse(json.dumps({'message': message}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_savelike(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        user_email = request.GET['email']
        post_id = request.GET['postid']

        users = User.objects.filter(email=user_email)
        if len(users) > 0:
            user = users[0]
            posts = ApiPost.objects.filter(PostId=post_id)
            if len(posts) > 0:
                post = posts[0]
                likes = ApiLikes.objects.filter(LikedPostId=post, LikerId=user)
                if len(likes) == 0:
                    like = ApiLikes.objects.create(LikedPostId=post, LikerId=user)
                    return HttpResponse(json.dumps({'message': 'Like Recorded!'}))
                else:
                    return HttpResponse(json.dumps({'message': 'This user has already liked this post!'}))
            else:
                return HttpResponse(json.dumps({'message': 'Invalid Post!'}))
        else:
            return HttpResponse(json.dumps({'message': 'Invalid User!'}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))


def api_savecomment(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        user_email = request.GET['email']
        post_id = request.GET['postid']
        comment = request.GET['comment']

        users = User.objects.filter(email=user_email)
        if len(users) > 0:
            user = users[0]
            posts = ApiPost.objects.filter(PostId=post_id)
            if len(posts) > 0:
                post = posts[0]
                new_comment = ApiComments.objects.create(PostId=post, CommentorId=user, Comment=comment, Time=datetime.datetime.now())
                return HttpResponse(json.dumps({'message': 'Comment Recorded!'}))
            else:
                return HttpResponse(json.dumps({'message': 'Invalid Post!'}))
        else:
            return HttpResponse(json.dumps({'message': 'Invalid User!'}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))
def api_sendfriendrequest(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        s_email=request.GET['sender']
        r_email=request.GET['receiver']
        user1=User.objects.get(email=s_email)
        user2=User.objects.get(email=r_email)
        allrequests1 = ApiFriendRequests.objects.filter(Sender=user1,Receiver=user2)
        allrequests2 = ApiFriendRequests.objects.filter(Sender=user2,Receiver=user1)
        if len(allrequests1)==0 and len(allrequests2)==0:
            req=ApiFriendRequests.objects.create(Sender=user1, Receiver=user2)
            return HttpResponse(json.dumps({'message':'Request Sent'}))
        else:
            return HttpResponse(json.dumps({'message': 'Request Already Exists'}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))
def api_requestresponse(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        s_email = request.GET['sender']
        r_email = request.GET['receiver']
        response=request.GET['response']
        user1 = User.objects.get(email=s_email)
        user2 = User.objects.get(email=r_email)
        allrequests = ApiFriendRequests.objects.filter(Sender=user1, Receiver=user2)
        if len(allrequests) > 0:
            if response=='Accept':
                t1 = ApiFriendship.objects.create(Friend_1=user1, Friend_2=user2)
                t1 = ApiFriendship.objects.create(Friend_1=user2, Friend_2=user1)
                r1 = ApiFriendRequests.objects.get(Sender=user1, Receiver=user2)
                r1.delete()
                return HttpResponse(json.dumps({'message': 'Request accepted!'}))
            elif response=='Reject':
                r1 = ApiFriendRequests.objects.get(Sender=user1, Receiver=user2)
                r1.delete()
                return HttpResponse(json.dumps({'message': 'Request rejected!'}))
        else:
            return HttpResponse(json.dumps({'message': 'Request does not exist!'}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))

def api_deletefriendrequest(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        s_email=request.GET['sender']
        r_email=request.GET['receiver']
        user1=User.objects.get(email=s_email)
        user2=User.objects.get(email=r_email)
        allrequests= ApiFriendRequests.objects.filter(Sender=user1,Receiver=user2)
        if len(allrequests)>0:
            r1 = ApiFriendRequests.objects.get(Sender=user1, Receiver=user2)
            r1.delete()
            return HttpResponse(json.dumps({'message': 'Request deleted!'}))
        else:
            return HttpResponse(json.dumps({'message': 'Request does not exist!'}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))
def api_removefriend(request):
    try:
        key = request.GET['api-key']
    except Exception as e:
        return HttpResponse(json.dumps({'message': 'Please provide api-key!'}))
    if key == API_KEY:
        friend1 = request.GET['friend1']
        friend2 = request.GET['friend2']
        user1 = User.objects.get(email=friend1)
        user2 = User.objects.get(email=friend2)
        r1 = ApiFriendship.objects.filter(Friend_1=user1, Friend_2=user2)
        if len(r1)>0:
            u1=ApiFriendship.objects.get(Friend_1=user1, Friend_2=user2)
            u2=ApiFriendship.objects.get(Friend_1=user2, Friend_2=user1)
            u1.delete()
            u2.delete()
            return HttpResponse(json.dumps({'message': 'Friend Removed!'}))
        else:
            return HttpResponse(json.dumps({'message': 'Friend does not exist!'}))
    else:
        return HttpResponse(json.dumps({'message': 'Invalid Api Key!'}))