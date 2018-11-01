from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    tx_url = models.CharField(max_length=80, blank=True)

    class Meta(AbstractUser.Meta):
        pass


class Profile(models.Model):
    user_pro = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=8, blank=True)
    introduce = models.CharField(max_length=40, blank=True)
    collects = models.ManyToManyField('post.Post', blank=True)
    name_show = models.SmallIntegerField(default=0)
    email_show = models.SmallIntegerField(default=0)
    follow_show = models.SmallIntegerField(default=0)
    collects_show = models.SmallIntegerField(default=0)


class MsgCategory(models.Model):
    name = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')     # 发送者
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')     # 发送给谁
    category = models.ForeignKey(MsgCategory, on_delete=models.CASCADE)     # 消息种类
    content = models.TextField(blank=True)       # 消息内容
    is_read = models.SmallIntegerField(default=0)   # 是否已读
    is_delete = models.SmallIntegerField(default=0)     # 是否删除
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.from_user.username

    class Meta:
        ordering = ['-created_time']


class MsgPost(models.Model):
    message = models.OneToOneField(Message, primary_key=True, on_delete=models.CASCADE)
    # 消息相关连的可能的是被关注者和文章、文章评论，我们分别与User和Post相关连,
    # 如果消息类别是被关注提醒，那么相关的用户是to_user所以可以不必再做关联
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title


class MailBox(models.Model):
    message = models.OneToOneField(Message, primary_key=True, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content[0:20]


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')   # 关注者
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')   # 被关注者

    class Meta:
        unique_together = (('follower', 'followed'), )


class EmailNotification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    praise = models.SmallIntegerField(default=0)
    followed = models.SmallIntegerField(default=0)
    comment = models.SmallIntegerField(default=1)
    collected = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    name = models.CharField(max_length=100)  # 标签名

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)  # 标签名

    def __str__(self):
        return self.name


