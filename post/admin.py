from django.contrib import admin
from .models import  Post, PostComent


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'user']


admin.site.register(Post)
admin.site.register(PostComent, PostCommentAdmin)
