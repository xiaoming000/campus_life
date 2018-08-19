from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import strip_tags
from django.urls import reverse
import markdown


class User(AbstractUser):
    tx_url = models.CharField(max_length=80, blank=True)

    class Meta(AbstractUser.Meta):
        pass


class Tag(models.Model):
    name = models.CharField(max_length=100)  # 标签名

    def __str__(self):
        return self.name


class News(models.Model):
    news_title = models.CharField(max_length=40)
    news_content = models.TextField()
    news_created_time = models.DateTimeField()
    news_modified_time = models.DateTimeField()
    news_delete = models.SmallIntegerField(default=0)
    excerpt = models.CharField(max_length=300, blank=True)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    auther = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.news_title

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_absolute_url(self):
        return reverse('users:news_detail', kwargs={'pk': self.pk})

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
            self.excerpt = strip_tags(md.convert(self.news_content))[:250]

        # 调用父类的 save 方法将数据保存到数据库中
        super(News, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-news_created_time']
