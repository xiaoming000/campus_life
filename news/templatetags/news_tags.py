from django import template
from ..models import News
# from users.models import Tag

register = template.Library()


@register.simple_tag
def get_recent_news(num=5):
    return News.objects.filter(talk=False).order_by('-created_time')[:num]


@register.simple_tag
def get_recent_talk(num=5):
    # tags = Tag.objects.filter(name='话题讨论')
    return News.objects.filter(talk=True).order_by('-created_time')[:num]