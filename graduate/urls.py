from django.conf.urls import url
from .views import GraduateView


app_name = 'graduate'
urlpatterns = [
    url(r'^$', GraduateView.as_view(), name='graduate_list')
]