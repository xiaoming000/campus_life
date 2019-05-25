import json

import redis
from django import template
from ..models import News
from ..spider import NewsSpider

register = template.Library()


@register.simple_tag
def get_recent_news(num=5):
    return News.objects.filter(talk=False).order_by('-created_time')[:num]


@register.simple_tag
def get_recent_talk(num=5):
    # tags = Tag.objects.filter(name='话题讨论')
    return News.objects.filter(talk=True).order_by('-created_time')[:num]


@register.simple_tag
def get_baidu_news():
    rd = redis.Redis(host='127.0.0.1', port=6379)
    result = rd.lrange('campus_baidu_news', 0, -1)
    response = []
    for res in result:
        response.append(json.loads(res))
    return response


@register.simple_tag
def get_zhihu_news():
    rd = redis.Redis(host='127.0.0.1', port=6379)
    result = rd.lrange('campus_zhihu_news', 0, -1)
    response = []
    for res in result:
        response.append(json.loads(res))
    return response


