from django.conf.urls import url
from . import views


app_name = 'users'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^info/(?P<pk>[0-9]+)/$', views.InfoView.as_view(), name='info'),

    url(r'^edit/(?P<pk>[0-9]+)/$', views.EditView.as_view(), name='edit'),
    url(r'^edit_nav/$', views.edit_nav, name='edit_nav'),
    url(r'^edit_activate/(?P<user_pk>[0-9]+)/$', views.EditActivateView.as_view(), name='edit_activate'),
    url(r'^edit_notification/(?P<user_pk>[0-9]+)/$', views.EditNotificationView.as_view(), name='edit_notification'),

    url(r'^edit_user_del/(?P<user_pk>[0-9]+)/$', views.EditUserDel.as_view(), name='edit_user_del'),
    url(r'^message/$', views.MessageView.as_view(), name='message'),
    url(r'^message_no_read/$', views.MessageNoReadView.as_view(), name='message_no_read'),
    url(r'^message_read/$', views.MessageReadView.as_view(), name='message_read'),
    url(r'^message_read_edit/$', views.message_read_edit, name='message_read_edit'),
]
