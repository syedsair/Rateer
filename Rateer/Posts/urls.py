from django.urls import path
from .views import PostsView, LikeView, CommentView, ShareView, DelView, UploadView
app_name = "Posts"
urlpatterns = [
    path('', PostsView, name="PostsView"),
    path('like/', LikeView, name="LikeView"),
    path('upload/', UploadView, name="UploadView"),
    path('comment/', CommentView, name="CommentView"),
    path('share/', ShareView, name="ShareView"),
    path('delete/<int:pid>/', DelView, name="DelView"),
]
