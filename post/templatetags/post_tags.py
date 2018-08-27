from django import template
from ..models import Post

register = template.Library()


@register.simple_tag
def get_recent_post(auther,):
    return Post.objects.filter(auther=auther).order_by('-created_time')[:5]


@register.simple_tag
def get_recent_wall(num=5):
    return Post.objects.filter(category=1).order_by('-created_time')[:num]


@register.simple_tag
def get_recent_study(num=5):
    return Post.objects.filter(category=2).order_by('-created_time')[:num]

