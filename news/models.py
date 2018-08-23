import markdown
from django.db import models
from django.utils.html import strip_tags
from django.urls import reverse
from users.models import User, Tag


class News(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    delete = models.SmallIntegerField(default=0)
    excerpt = models.CharField(max_length=300, blank=True)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    auther = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'pk': self.pk})

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
            self.excerpt = strip_tags(md.convert(self.content))[:250]

        # 调用父类的 save 方法将数据保存到数据库中
        super(News, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']


class NewsComent(models.Model):
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    delete = models.SmallIntegerField(default=0)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
