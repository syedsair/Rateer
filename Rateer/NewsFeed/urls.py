from django.urls import path
from .views import NewsFeedView, LikeView, CommentView, ShareView
app_name = "NewsFeed"
urlpatterns = [
    path('', NewsFeedView, name="NewsFeedView"),
    path('like/', LikeView, name="LikeView"),
    path('comment/', CommentView, name="CommentView"),
    path('share/', ShareView, name="ShareView"),
]
