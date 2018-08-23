from django import template
from ..models import News

register = template.Library()


@register.simple_tag
def get_recent_news(num=5):
    return News.objects.all().order_by('-created_time')[:num]