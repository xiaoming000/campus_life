import json
import redis
import markdown
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from .forms import NewsCommentForm, NewsReplyForm
from .models import News, NewsComment, Reply
from users.models import MsgCategory, MailBox, Message, EmailNotification
from users.email import CreateMessage
from .spider import NewsSpider


class NewsView(View):
    def get(self, request):
        news = News.objects.all()
        return render(request, 'news/news.html', {
            'news': news,
            'htitle': '校园新闻',
        })


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/detail.html'
    content_object_name = 'news'

    def get(self, request, *args, **kwargs):
        response = super(NewsDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        news = super(NewsDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            TocExtension(slugify=slugify),
        ])
        news.content = md.convert(news.content)
        news.toc = md.toc
        return news

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        news = super(NewsDetailView, self).get_object(queryset=None)
        tags_list = news.tags.all()
        form = NewsCommentForm()
        comment_list = news.newscomment_set.all()
        context.update({
            'tags_list': tags_list,
            'nav': 2,
            'htitle': '校园新闻-' + news.title,
            'form': form,
            'comment_list': comment_list
        })
        return context


def news_comment(request, news_pk):
    news = get_object_or_404(News, pk=news_pk)
    user = request.user
    if request.method == 'POST':
        form = NewsCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.user = user
            comment.save()

            content = request.POST['content']
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            content = md.convert(content)
            category = MsgCategory.objects.get(name='comment')
            news_url = request.build_absolute_uri(news.get_absolute_url())
            msg = CreateMessage(from_user=request.user, to_user=news.auther, category=category, content=content, news_url=news_url)
            msg.create_email()

            return redirect(news)
        else:
            comment_list = news.newscomment_set.all()
            context = {
                'newst': news,
                'form': form,
                'comment_list': comment_list
            }
            return render(request, 'news/detail.html', context=context)
    return redirect(news)


def news_reply(request, news_pk):
    news = get_object_or_404(News, pk=news_pk)
    user = request.user
    if request.method == "POST":
        reply_form = NewsReplyForm(request.POST)
        if reply_form.is_valid():
            reply_form = reply_form.save(commit=False)
            if request.POST['comment_reply']:
                reply_form.comment_reply = Reply.objects.filter(pk=request.POST['comment_reply'])[0]
            reply_form.user = user
            reply_form.save()

            return redirect(news)
        else:
            comment_list = news.newscomment_set.all()
            context = {
                'post': news,
                'form': NewsReplyForm(),
                'reply_form': reply_form,
                'comment_list': comment_list
            }
        return render(request, 'news/detail.html', context=context)
    return redirect(news)


@login_required()
def del_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id', '')
        response = ""
        try:
            comment = NewsComment.objects.get(pk=comment_id)
            if comment.user == request.user or request.user.is_staff:
                NewsComment.objects.filter(pk=comment_id).delete()
                response = "删除成功！"
        except:
            response = "删除失败！"

        return HttpResponse(json.dumps(response), content_type="application/json")


# 删除操作
@login_required()
def del_reply(request):
    if request.method == 'POST':
        reply_id = request.POST.get('reply_id', '')
        response = ""
        try:
            reply = Reply.objects.get(pk=reply_id)
            if reply.user == request.user or request.user.is_staff:
                Reply.objects.filter(pk=reply_id).delete()
                response = "删除成功！"
        except:
            response = "删除失败！"
        return HttpResponse(json.dumps(response), content_type="application/json")


def news_spider(request):
    spider = NewsSpider()
    # 百度新闻
    baidu_url = "http://top.baidu.com/index.html"
    rd = redis.Redis(host='127.0.0.1', port=6379)
    response = spider.get_baidu_news(baidu_url)
    if len(response) > 0:
        rd.delete('campus_baidu_news')
        for res in response:
            data = json.dumps(res)
            rd.rpush('campus_baidu_news', data)
    # 知乎热搜
    # zhihu_url = "https://www.zhihu.com/hot"
    # response = spider.get_zhihu_news(zhihu_url)
    # if len(response) > 0:
    #     rd.delete('campus_zhihu_news')
    #     for res in response:
    #         data = json.dumps(res)
    #         rd.rpush('campus_zhihu_news', data)
    return HttpResponse("执行成功", content_type="application/json")
