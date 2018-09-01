from django.conf.urls import url
from .views import UserAjax, Register, Login, Index, loginout, verifycode, InfoView


app_name = 'users'
urlpatterns = [
    url(r'^userajax/$', UserAjax, name='userajax'),
    url(r'^register/$', Register, name='register'),
    url(r'^login/$', Login, name='login'),
    url(r'^$', Index, name='index'),
    url(r'^loginout/$', loginout, name='loginout'),
    url(r'^verifycode/$', verifycode, name='verifycode'),
    url(r'^info/$', InfoView.as_view(), name='info'),
]