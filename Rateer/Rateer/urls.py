from django.contrib import admin
from django.conf.urls.static import static
from . import settings
from django.urls import path, include
from Home import urls as home_urls
from Posts import urls as post_urls
from NewsFeed import urls as nf_urls
from Dashboard import urls as dashboard_urls
from Friends import urls as friends_urls
from Messenger import urls as messenger_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(home_urls, namespace="Home")),
    path('home/', include(home_urls, namespace="Home")),
    path('dashboard/', include(dashboard_urls, namespace="Dashboard")),
    path('posts/', include(post_urls, namespace='Posts')),
    path('newsfeed/', include(nf_urls, namespace='NewsFeed')),
    path('friends/', include(friends_urls, namespace="Friends")),
    path('messenger/', include(messenger_urls, namespace="Messenger")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)