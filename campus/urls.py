"""campus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from post.views import upload_img

urlpatterns = [
    path('upload_img/', upload_img),  # 后台富文本框上传图片
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('news/', include('news.urls')),
    path('post/', include('post.urls')),
    path('graduate/', include('graduate.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    path('search/', include('haystack.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
