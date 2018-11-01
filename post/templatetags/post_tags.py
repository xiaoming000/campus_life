from django import template
from ..models import Post

register = template.Library()


# 获取作者最近发表的文章
@register.simple_tag
def get_recent_post(author, num=5):
    return Post.objects.filter(author=author).order_by('-created_time')[:num]


# 获取作者最近发表的文章
@register.simple_tag
def get_recent_post_all(author):
    return Post.objects.filter(author=author).order_by('-created_time')


# 获取最近的万能墙
@register.simple_tag
def get_recent_wall(num=5):
    return Post.objects.filter(category=1).order_by('-created_time')[:num]


# 获取最近的学习交流的文章
@register.simple_tag
def get_recent_study(num=5):
    return Post.objects.filter(category=2).order_by('-created_time')[:num]


# 获取文章的第一章图片
@register.simple_tag
def get_post_img_first(post):
    images = post.postimg_set.all()
    if len(images) > 1:
        images = images.first()
    return images


# 获取文章的全部图片
@register.simple_tag
def get_post_img(post):
    images = post.postimg_set.all()
    return images
