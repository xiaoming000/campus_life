from django.conf.urls import url
from .views import PostView, PostDetailView, StudyView, \
    post_comment, Push, post_reply, del_comment, del_reply, WallView, LikeView, CollectView, add_tags, post_del


app_name = 'post'
urlpatterns = [
    url(r'^wall/$', PostView.as_view(), name='wall'),
    url(r'^detail/(?P<pk>[0-9]+)/$', PostDetailView.as_view(), name='detail'),
    url(r'^wall_detail/(?P<pk>[0-9]+)/$', WallView.as_view(), name='wall_detail'),
    url(r'^study/$', StudyView.as_view(), name='study'),
    url(r'^post_comment/(?P<post_pk>[0-9]+)/$', post_comment, name='post_comment'),
    url(r'^post_reply/(?P<post_pk>[0-9]+)/$', post_reply, name='post_reply'),
    url(r'^push/$', Push.as_view(), name='push'),
    url(r'^del_comment/$', del_comment, name='del_comment'),
    url(r'^del_reply/$', del_reply, name='del_reply'),
    url(r'^likes/$', LikeView.as_view(), name='likes'),
    url(r'^collects/$', CollectView.as_view(), name='collects'),

    url(r'^add_tags/$', add_tags, name='add_tags'),
    url(r'^post_del/$', post_del, name='post_del'),
]