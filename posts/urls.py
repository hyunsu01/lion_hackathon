# posts/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from posts.views import PostViewSet
from django.conf import settings
from django.conf.urls.static import static
from . import views


router = routers.DefaultRouter()
router.register('Post', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

