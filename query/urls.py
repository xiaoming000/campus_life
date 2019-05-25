from django.conf.urls import url
from .views import course_login, courses, grade_login


app_name = 'query'
urlpatterns = [
    url(r'^course_login/$', course_login, name='course_login'),
    url(r'^grade_login/$', grade_login, name='grade_login'),
    url(r'^courses/$', courses, name='courses'),
]