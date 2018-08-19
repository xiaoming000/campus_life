from django.conf.urls import url
from .views import NewsView, UserAjax, Register, Login
from django.urls import path


app_name = 'users'
urlpatterns = [
    url(r'^news/$', NewsView.as_view(), name='news'),
    url(r'^userajax/$', UserAjax, name='userajax'),
    url(r'^register/$', Register, name='register'),
    url(r'^login/$', Login, name='login')
]