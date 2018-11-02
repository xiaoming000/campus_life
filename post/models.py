import markdown
from django.db import models
from django.utils.html import strip_tags
from django.urls import reverse
from users.models import User, Tag, Category


class Post(models.Model):

    title = models.CharField(max_length=40)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now_add=True)
    delete = models.SmallIntegerField(default=0)
    excerpt = models.CharField(max_length=300, blank=True)
    anonymous = models.SmallIntegerField(default=0)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    collects = models.ManyToManyField(User, blank=True, related_name='collects')

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_absolute_url(self):
        if self.category.name == '学习交流':
            return reverse('post:detail', kwargs={'pk': self.pk})
        elif self.category.name == '万能墙':
            return reverse('post:wall_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.content)).replace(' ', '')[:250]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']


class PostImg(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    filename = models.CharField(max_length=200, blank=True, null=True)
    url = models.ImageField(upload_to='./media')

    def __str__(self):
        return self.post.title


class PostComment(models.Model):
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    delete = models.SmallIntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20]


class PostReply(models.Model):

    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    delete = models.SmallIntegerField(default=0)
    reply_type = models.SmallIntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    comment_reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.text[0:20]





