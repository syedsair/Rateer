from django.shortcuts import render, redirect
from .models import Posts, Comments, Likes
from Dashboard.models import NotificationStatus
from Friends.models import Friendship
from django.contrib.auth.models import User
from datetime import datetime
from django.http import HttpResponseRedirect


# Create your views here.
def PostsView(request):
    user = request.user
    posts = Posts.objects.filter(Poster=user)
    likes = []
    comments = []
    contents = []
    Commentss = Comments.objects.none()
    Likess = Likes.objects.none()

    for post in posts:
        newQuerySet = Comments.objects.filter(LikedPostId=post)
        Commentss = (Commentss | newQuerySet)

    for post in posts:
        newQuerySet = Likes.objects.filter(LikedPostId=post)
        Likess = (Likess | newQuerySet)
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
    ms = status.Messenger
    fr = status.Requests
    nf = status.Feed
    data_dict = {
        'person_name': user.username,
        'no_of_posts': len(posts),
        'posts': posts,
        'contents': contents,
        'likes': likes,
        'comments': comments,
        'Comments': Commentss,
        'Likes': Likess,
        'LikedPosts':LikedPosts,
        'ms':ms,
        'nf':nf,
        'fr':fr
    }
    return render(request, 'Posts.html', context=data_dict)


def LikeView(request):
    liker = User.objects.get(username=request.POST.get("liker"))
    post = Posts.objects.get(PostId=request.POST.get("post_id"))

    instance = Likes.objects.filter(LikerPid=liker, LikedPostId=post)
    if len(instance) == 0:
        like = Likes.objects.create(LikerPid=liker, LikedPostId=post)
        like.save()
    else:
        instance.delete()

    #return redirect(request.META['HTTP_REFERER'])
    return HttpResponseRedirect("/posts/")


def CommentView(request):
    comment = request.POST.get("comment")
    post = Posts.objects.get(PostId=request.POST.get("post_id"))
    time = datetime.now()
    liker = request.user

    CommentObj = Comments.objects.create(LikedPostId=post, LikerPid=liker, Comment=comment, Time=time)
    CommentObj.save()

    return HttpResponseRedirect("/posts/")


def ShareView(request):
    post = Posts.objects.get(PostId=request.POST.get("post_id"))

    new_post = Posts.objects.create(Poster=request.user, Content=post.Content, Caption="", Event="shared a post.", Time=datetime.now())
    new_post.save()

    return HttpResponseRedirect("/posts/")


def DelView(request, pid):
    post = Posts.objects.get(PostId=pid)
    if post:
        post.delete()
    return HttpResponseRedirect("/posts/")


def UploadView(request):
    caption = request.POST.get('caption')
    content = request.FILES['contentpost']
    post = Posts.objects.create(Poster = request.user, Content = content, Caption = caption, Event="uploaded a post.", Time = datetime.now())
    post.save()

    frienships = Friendship.objects.filter(Friend_1=request.user)
    for frienship in frienships:
        user = frienship.Friend_2
        status = NotificationStatus.objects.filter(ThisUser=user)[0]
        status.Feed = True
        status.save()

    return HttpResponseRedirect("/posts/")
