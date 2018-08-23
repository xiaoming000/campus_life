from django import template
from ..models import Post

register = template.Library()


@register.simple_tag
def get_recent_post(auther,):
    return Post.objects.filter(auther=auther).order_by('-created_time')[:5]

