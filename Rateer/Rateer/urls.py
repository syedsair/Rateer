from django.contrib import admin
from django.conf.urls.static import static
from . import settings
from django.urls import path, include
from Api import urls as api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(api_urls)),
    path('api/', include(api_urls))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)