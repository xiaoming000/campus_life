import json

import markdown
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import View
from django.views.generic import DetailView
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from .forms import PostCommentForm, PostForm, PostReplyForm
from .models import Post, PostComment, PostReply, PostImg
from users.models import Category, Tag
from datetime import datetime


from django.views.decorators.csrf import csrf_exempt
import json
import time
from PIL import Image
from django.conf import settings
from django.http import HttpResponse


class PostView(View):
    def get(self, request):
        redirect_to = request.POST.get('next', request.GET.get('next', ''))
        post_list = Post.objects.filter(category=1)
        now_time = datetime.now()
        return render(request, 'post/post.html', {
            'post_list': post_list,
            'next': redirect_to,
            'fail': 0,
            'nav': 3,
            'htitle': '万能墙',
            'now_time': now_time
        })


class StudyView(View):
    def get(self, request):
        redirect_to = request.POST.get('next', request.GET.get('next', ''))
        study_list = Post.objects.filter(category=2)
        now_time = datetime.now()
        return render(request, 'post/study.html', {
            'study_list': study_list,
            'next': redirect_to,
            'fail': 0,
            'nav': 4,
            'htitle': '学习交流',
            'now_time': now_time
        })


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/detail.html'
    content_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            TocExtension(slugify=slugify),
        ])
        post.content = md.convert(post.content)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = super(PostDetailView, self).get_object(queryset=None)
        tags_list = post.tags.all()
        form = PostCommentForm()
        reply_form = PostReplyForm()
        comment_list = post.postcomment_set.all()
        reply_list = []
        if post.category.pk == 1:
            title = '万能墙'
            nav = 3
        else:
            title = '学习交流'
            nav = 4
        context.update({
            'tags_list': tags_list,
            'nav': nav,
            'form': form,
            'reply_form': reply_form,
            'comment_list': comment_list,
            'reply_list': reply_list,
            'htitle': title + '-' + post.title,
        })
        return context


# 可能要重构
def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user
    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()

            return redirect(post)
        else:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
                TocExtension(slugify=slugify),
            ])
            post.content = md.convert(post.content)
            post.toc = md.toc
            comment_list = post.postcomment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
        return render(request, 'post/detail.html', context=context)

    return redirect(post)


def post_reply(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user
    if request.method == "POST":
        reply_form = PostReplyForm(request.POST)
        if reply_form.is_valid():
            reply_form = reply_form.save(commit=False)
            if request.POST['comment_reply']:
                reply_form.comment_reply = PostReply.objects.filter(pk=request.POST['comment_reply'])[0]
            reply_form.user = user
            reply_form.save()

            return redirect(post)
        else:
            comment_list = post.postcomment_set.all()
            context = {
                'post': post,
                'form': PostReplyForm(),
                'reply_form': reply_form,
                'comment_list': comment_list
            }
        return render(request, 'news/detail.html', context=context)
    return redirect(post)


# 删除评论
@login_required()
def del_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id', '')
        response = ""
        try:
            comment = PostComment.objects.get(pk=comment_id)
            if comment.user == request.user or comment.post.author == request.user or request.user.is_staff:
                PostComment.objects.filter(pk=comment_id).delete()
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
            reply = PostReply.objects.get(pk=reply_id)
            if reply.user == request.user or reply.comment.post.author == request.user or request.user.is_staff:
                PostReply.objects.filter(pk=reply_id).delete()
                response = "删除成功！"
        except:
            response = "删除失败！"

        return HttpResponse(json.dumps(response), content_type="application/json")


def push_wall(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    category_id = request.POST.get('category', request.GET.get('category', ''))
    if not category_id:
        category_id = 1
    if request.method == 'POST':
        form = PostForm(request.POST)
        category = Category.objects.filter(pk=category_id)
        tags_str = request.POST['tags_str']
        tags_list = tags_str.split(',')
        tags_push = []
        for tag in tags_list:
            tags_data = Tag.objects.filter(name=tag)
            if tags_data:
                tags = tags_data[0]
                tags_push.append(tags)
            else:
                tags = Tag()
                tags.name = tag
                tags.save()
                tags_push.append(tags)
        # return HttpResponse(request.POST['next'])
        if form.is_valid():
            post = form.save(commit=False)
            post.category = category[0]
            post.author = request.user
            post.save()
            post.tags.set(tags_push)
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # return HttpResponse(redirect_to)
        form = PostForm()
        context = {
            'form': form,
            'next': redirect_to,
            'category': category_id
        }
    return render(request, 'post/push_wall.html', context=context)


static_base = 'http://127.0.0.1:8000'
static_url = static_base + settings.MEDIA_URL  # 上传文件展示路径前缀


# 上传图片 POST
@csrf_exempt
def upload_img(request):
    file = request.FILES['file']
    data = {
        'error': True,
        'path': '',
    }
    if file:
        timenow = int(time.time()*1000)
        timenow = str(timenow)
        try:
            img = Image.open(file)
            img.save(settings.MEDIA_ROOT + "content/" + timenow + str(file))
            # post_img = PostImg()
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps(data), content_type="application/json")
        imgUrl = static_url + 'content/' + timenow + str(file)
        data['error'] = False
        data['path'] = imgUrl
    return HttpResponse(json.dumps(data), content_type="application/json")

