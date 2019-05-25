from django.contrib import admin
from .models import Course, QueryUsers


class CourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'xnd', 'xqd']


class QueryUsersAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Course, CourseAdmin)
admin.site.register(QueryUsers, QueryUsersAdmin)
