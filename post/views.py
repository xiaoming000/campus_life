import json
import time
import markdown
import re
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import View
from django.views.generic import DetailView, ListView
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from .forms import PostCommentForm, PostForm, PostReplyForm
from .models import Post, PostComment, PostReply, PostImg
from users.models import Category, Tag
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from django.conf import settings


class PostView(ListView):
    model = Post
    template_name = 'post/post.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        post_list = super(PostView, self).get_queryset().filter(category=1)
        for post in post_list:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
                TocExtension(slugify=slugify),
            ])
            post.content = md.convert(post.content)
            # 将文章中的img去掉
            images = r'(<img){1}(.)*?(/>){1}'
            post.content = re.sub(images, '', post.content)
            # # 取出文章的前6行显示在列表中
            post_list_all = post.content.split(r'<br />')
            post_part = '<br />'.join(post_list_all[0:5])
            post.content = post_part
            post.content_all = '<br />'.join(post_list_all)
        return post_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context.update({
            'htitle': '万能墙',
        })
        return context


class StudyView(View):
    def get(self, request):
        study_list = Post.objects.filter(category=2)
        return render(request, 'post/study.html', {
            'study_list': study_list,
            'htitle': '学习交流',
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
        context.update({
            'tags_list': tags_list,
            'form': form,
            'reply_form': reply_form,
            'comment_list': comment_list,
            'reply_list': reply_list,
            'htitle': post.category.name + '-' + post.title,
        })
        return context


class WallView(PostDetailView):
    model = Post
    template_name = 'post/wall.html'
    content_object_name = 'post'


@login_required()
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


@login_required()
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


def push(request):
    # redirect_to = request.POST.get('next', request.GET.get('next', ''))
    category_id = request.POST.get('category', request.GET.get('category', ''))
    if not category_id:
        category_id = 1
    if request.method == 'POST':
        post_img = request.POST.get('post_img', '')
        post_img_list = post_img.split()

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
                try:
                    tags = Tag()
                    tags.name = tag
                    tags.save()
                    tags_push.append(tags)
                except Exception as e:
                    print(e)
                    raise Http404

        if form.is_valid():
            post = form.save(commit=False)
            post.category = category[0]
            post.author = request.user
            post.save()
            post.tags.set(tags_push)

            try:
                # 保存post图片地址
                for img in post_img_list:
                    post_img = PostImg()
                    post_img.post = post
                    post_img.filename = img
                    post_img.url = img
                    post_img.save()
            except Exception as e:
                print(e)
                raise Http404
            # 保存文章

            return redirect(post)
    else:
        form = PostForm()
        context = {
            'form': form,
            'category': category_id
        }
        return render(request, 'post/push.html', context=context)


# 上传图片 POST
@csrf_exempt
def upload_img(request):
    static_base = str(get_current_site(request).domain)[0:-1]
    static_url = static_base + settings.MEDIA_URL  # 上传文件展示路径前缀

    file = request.FILES['file']
    data = {
        'error': True,
        'path': '',
    }
    if file:
        time_now = int(time.time()*1000)
        time_now = str(time_now)
        img_url = static_url + 'content/' + time_now + str(file)
        try:
            img = Image.open(file)
            img.save(settings.MEDIA_ROOT + "content/" + time_now + str(file))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps(data), content_type="application/json")
        data['error'] = False
        data['path'] = img_url
    return HttpResponse(json.dumps(data), content_type="application/json")

