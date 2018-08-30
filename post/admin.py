from django.contrib import admin
from .models import  Post, PostComent, PostReply


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'user']


class PostReplyAdmin(admin.ModelAdmin):
    list_display = ['content', 'user', 'created_time']


admin.site.register(Post)
admin.site.register(PostComent, PostCommentAdmin)
admin.site.register(PostReply, PostReplyAdmin)
