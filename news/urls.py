from django.conf.urls import url
from .views import NewsDetailView, NewsView, news_comment, news_reply, del_reply, del_comment, news_spider


app_name = 'news'
urlpatterns = [
    url(r'^$', NewsView.as_view(), name='news_list'),
    url(r'^detail/(?P<pk>[0-9]+)/$', NewsDetailView.as_view(), name='detail'),
    url(r'^news_comment/(?P<news_pk>[0-9]+)/$', news_comment, name='news_comment'),
    url(r'^news_reply/(?P<news_pk>[0-9]+)/$', news_reply, name='news_reply'),
    url(r'^del_comment/$', del_comment, name='del_comment'),
    url(r'^del_reply/$', del_reply, name='del_reply'),
    url(r'^news_spider/$', news_spider, name='news_spider'),
]