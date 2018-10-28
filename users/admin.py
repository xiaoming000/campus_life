from django.contrib import admin
from .models import User, Tag, Category, Profile, Follow, Message, MsgCategory, MsgPost, EmailNotification, MailBox


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_pro']


admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follow)
admin.site.register(Message)
admin.site.register(MsgCategory)
admin.site.register(MsgPost)
admin.site.register(EmailNotification)
admin.site.register(MailBox)