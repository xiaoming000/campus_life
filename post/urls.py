from django.conf.urls import url
from .views import PostView, PostDetailView, StudyView, post_comment, push_wall, post_reply


app_name = 'post'
urlpatterns = [
    url(r'^wall/$', PostView.as_view(), name='wall'),
    url(r'^detail/(?P<pk>[0-9]+)/$', PostDetailView.as_view(), name='detail'),
    url(r'^study/$', StudyView.as_view(), name='study'),
    url(r'^post_comment/(?P<post_pk>[0-9]+)/$', post_comment, name='post_comment'),
    url(r'^post_reply/(?P<post_pk>[0-9]+)/$', post_reply, name='post_reply'),
    url(r'^push_wall$', push_wall, name='push_wall'),
]