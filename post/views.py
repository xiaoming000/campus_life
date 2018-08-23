import markdown
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from users.forms import RegisterForm
from .forms import PostCommentForm
from .models import Post, PostComent


class PostView(View):
    def get(self, request):
        form = RegisterForm()  # 渲染注册空表单
        redirect_to = request.POST.get('next', request.GET.get('next', ''))
        post_list = Post.objects.filter(category=1)
        return render(request, 'post/post.html', {
            'form': form,
            'post_list': post_list,
            'next': redirect_to,
            'fail': 0,
            'nav': 3,
            'htitle': '万能墙'
        })


class StudyView(View):
    def get(self, request):
        form = RegisterForm()  # 渲染注册空表单
        redirect_to = request.POST.get('next', request.GET.get('next', ''))
        study_list = Post.objects.filter(category=2)
        return render(request, 'post/study.html', {
            'form': form,
            'study_list': study_list,
            'next': redirect_to,
            'fail': 0,
            'nav': 4,
            'htitle': '学习交流'
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
        comment_list = post.postcoment_set.all()
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
            'comment_list': comment_list,
            'htitle': title +'-' + post.title
        })
        return context


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
            comment_list = post.postcoment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
        return render(request, 'post/detail.html', context=context)

    return redirect(post)



