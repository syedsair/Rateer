from django.shortcuts import render
from django.contrib.auth.models import User
from Posts.models import Posts, Comments, Likes
from Friends.models import Friendship
from Dashboard.models import NotificationStatus
from django.http import HttpResponseRedirect
from datetime import datetime


# Create your views here.
def NewsFeedView(request):
    user = request.user
    friends = Friendship.objects.filter(Friend_1=user)
    posts = Posts.objects.none()
    Commentss = Comments.objects.none()
    Likess = Likes.objects.none()

    for friend in friends:
        newQuerySet = Posts.objects.filter(Poster=friend.Friend_2).order_by('-Time')
        posts = (posts | newQuerySet)

    for post in posts:
        newQuerySet = Comments.objects.filter(LikedPostId=post)
        Commentss = (Commentss | newQuerySet)

    for post in posts:
        newQuerySet = Likes.objects.filter(LikedPostId=post)
        Likess = (Likess | newQuerySet)

    likes = []
    comments = []
    contents = []
    for i in range(len(posts)):
        likes.append(len(Likes.objects.filter(LikedPostId=posts[i])))
        comments.append(len(Comments.objects.filter(LikedPostId=posts[i])))
        contents.append(posts[i].Content.url)

    LikedPosts = []
    for post in posts:
        if len(Likes.objects.filter(LikerPid=user, LikedPostId=post)) > 0:
            LikedPosts.append(post.PostId)
        else:
            pass

    status = NotificationStatus.objects.filter(ThisUser=user)[0]
    if status.Feed:
        status.Feed = False
        status.save()
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed
    data_dict = {
        'person_name': user.username,
        'posts': posts,
        'contents': contents,
        'likes': likes,
        'comments': comments,
        'Comments': Commentss,
        'Likes': Likess,
        'LikedPosts': LikedPosts,
        'ms': ms,
        'nf':nf,
        'fr':fr
    }
    return render(request, 'NewsFeed.html', context=data_dict)


def LikeView(request):
    print(request.POST.get("liker"))
    liker = User.objects.get(username=request.POST.get("liker"))
    post = Posts.objects.get(PostId=request.POST.get("post_id"))

    instance = Likes.objects.filter(LikerPid=liker, LikedPostId=post)
    if len(instance) == 0:
        like = Likes.objects.create(LikerPid=liker, LikedPostId=post)
        like.save()
    else:
        instance.delete()

    return HttpResponseRedirect("/newsfeed/")


def CommentView(request):
    comment = request.POST.get("comment")
    post = Posts.objects.get(PostId=request.POST.get("post_id"))
    time = datetime.now()
    liker = request.user

    CommentObj = Comments.objects.create(LikedPostId=post, LikerPid=liker, Comment=comment, Time=time)
    CommentObj.save()

    return HttpResponseRedirect("/newsfeed/")


def ShareView(request):
    post = Posts.objects.get(PostId=request.POST.get("post_id"))

    new_post = Posts.objects.create(Poster=request.user, Content=post.Content, Caption="", Event="shared a post.", Time=datetime.now())
    new_post.save()

    return HttpResponseRedirect("/newsfeed/")