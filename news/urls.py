from django.conf.urls import url
from .views import NewsDetailView, NewsView, news_comment


app_name = 'news'
urlpatterns = [
    url(r'^$', NewsView.as_view(), name='news_list'),
    url(r'^detail/(?P<pk>[0-9]+)/$', NewsDetailView.as_view(), name='detail'),
    url(r'^news_comment/(?P<news_pk>[0-9]+)/$', news_comment, name='news_comment'),
]