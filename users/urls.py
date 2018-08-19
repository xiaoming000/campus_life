from django.conf.urls import url
from .views import NewsView, UserAjax, Register, Login, NewsDetail
from django.urls import path


app_name = 'users'
urlpatterns = [
    url(r'^news/$', NewsView.as_view(), name='news'),
    url(r'^userajax/$', UserAjax, name='userajax'),
    url(r'^register/$', Register, name='register'),
    url(r'^login/$', Login, name='login'),
    url(r'^news_detail/(?P<pk>[0-9]+)/$', NewsDetail.as_view(), name='news_detail')
]