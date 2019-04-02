from .models import Message, MailBox, EmailNotification
from django.core.mail import EmailMultiAlternatives
from django.template import loader


class CreateMessage(object):

    def __init__(self, from_user, to_user, category, content, news_url):
        self.news_url = news_url
        self.message = Message()
        self.message.from_user = from_user
        self.message.to_user = to_user
        self.message.category = category
        self.message.content = content
        self.message.save()
        self.email_notification = EmailNotification.objects.get(user=self.message.to_user)

    def email_comment(self):
        if self.email_notification.comment == 1:

            email_box = MailBox(message=self.message)
            email_box.content = self.message.content
            email_box.save()
            content = self.message.content
            context = {
                'content': content,
                'news_url': self.news_url
            }
            html_content = loader.get_template('users/email_comment.html')
            text_content = "您的邮箱不支持多媒体文件！"
            msg = EmailMultiAlternatives("校园生活平台-通知", text_content, '664374295@qq.com', [self.message.to_user.email])
            msg.attach_alternative(html_content.render(context), "text/html")
            msg.send()

    def email_praise(self):
        if self.email_notification.praise == 1:
            email_box = MailBox(message=self.message)
            email_box.content = self.message.content
            email_box.save()
            content = self.message.content
            context = {
                'content': content
            }
            html_content = loader.get_template('users/email_praise.html')
            text_content = "您的邮箱不支持多媒体文件！"
            msg = EmailMultiAlternatives("校园生活平台-通知",text_content, '664374295@qq.com', [self.message.to_user.email])
            msg.attach_alternative(html_content.render(context), "text/html")
            msg.send()

    def email_followed(self):
        if self.email_notification.followed == 1:
            email_box = MailBox(message=self.message)
            email_box.content = self.message.content
            email_box.save()
            content = self.message.content
            context = {
                'content': content
            }
            html_content = loader.get_template('users/email_followed.html')
            text_content = "您的邮箱不支持多媒体文件！"
            msg = EmailMultiAlternatives("校园生活平台-通知",text_content, '664374295@qq.com', [self.message.to_user.email])
            msg.attach_alternative(html_content.render(context), "text/html")
            msg.send()

    def email_collected(self):
        if self.email_notification.collected == 1:
            email_box = MailBox(message=self.message)
            email_box.content = self.message.content
            email_box.save()
            content = self.message.content
            context = {
                'content': content
            }
            html_content = loader.get_template('users/email_collected.html')
            text_content = "您的邮箱不支持多媒体文件！"
            msg = EmailMultiAlternatives("校园生活平台-通知",text_content, '664374295@qq.com', [self.message.to_user.email])
            msg.attach_alternative(html_content.render(context), "text/html")
            msg.send()

    def create_email(self):
        if self.message.category.name == 'comment':
            self.email_comment()
        elif self.message.category.name == 'praise':
            self.email_praise()
        elif  self.message.category.name == 'followed':
            self.email_followed()
        elif self.message.category.name == 'collected':
            self.email_collected()

