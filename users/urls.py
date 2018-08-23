from django.conf.urls import url
from .views import UserAjax, Register, Login


app_name = 'users'
urlpatterns = [
    url(r'^userajax/$', UserAjax, name='userajax'),
    url(r'^register/$', Register, name='register'),
    url(r'^login/$', Login, name='login'),
]