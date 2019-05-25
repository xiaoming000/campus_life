from django.db import models
from users.models import User


class QueryUsers(models.Model):
    number = models.CharField(max_length=20)
    password = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_login_time = models.DateTimeField()


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    xnd = models.CharField(max_length=10)
    xqd = models.SmallIntegerField()
    number = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    faculty = models.CharField(max_length=40)
    major = models.CharField(max_length=40)
    a_class = models.CharField(max_length=40)
    course_table = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
