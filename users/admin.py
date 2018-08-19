from django.contrib import admin
from .models import User, Tag, News

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(News)