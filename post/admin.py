from django.contrib import admin
from .models import Post, PostComment, PostReply, PostImg


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'user']


class ReplyAdmin(admin.ModelAdmin):
    list_display = ['text', 'user', 'created_time']


class PostAdmin(admin.ModelAdmin):
    list_display = ['title']

    class Media:
        js = [
            '/static/js/jquery.min.js',   # 必须首先加载的jquery，手动添加文件
            '/static/js/tinymce/tinymce.min.js',   # tinymce自带文件
            '/static/js/jquery.form.js',    # 手动添加文件
            '/static/js/tinymce/textarea.js',   # 手动添加文件，用户初始化参数
        ]


admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(PostReply, ReplyAdmin)
admin.site.register(PostImg)
