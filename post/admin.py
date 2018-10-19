from django.contrib import admin
from .models import Post, PostComment, PostReply


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'user']


class ReplyAdmin(admin.ModelAdmin):
    list_display = ['text', 'user', 'created_time']


admin.site.register(Post)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(PostReply, ReplyAdmin)
