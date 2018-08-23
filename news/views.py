import markdown
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from users.forms import RegisterForm
from .forms import NewsCommentForm
from .models import News


class NewsView(View):
    def get(self, request):
        form = RegisterForm()  # 渲染注册空表单
        redirect_to = request.POST.get('next', request.GET.get('next', ''))
        news = News.objects.all()
        return render(request, 'news/news.html', {
            'form': form,
            'news': news,
            'next': redirect_to,
            'fail': 0,
            'htitle': '校园新闻',
            'nav': 2
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
        comment_list = news.newscoment_set.all()
        context.update({
            'tags_list': tags_list,
            'nav': 2,
            'htitle': '校园新闻-'+ news.title,
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

            return redirect(news)
        else:
            comment_list = news.newscoment_set.all()
            context = {
                'post': news,
                'form': form,
                'comment_list': comment_list
            }
        return render(request, 'news/detail.html', context=context)

    return redirect(news)
