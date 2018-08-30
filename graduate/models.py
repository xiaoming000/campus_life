from django.db import models
from users.models import User


class Graduate(models.Model):
    name = models.CharField(max_length=30)  # 姓名
    profession = models.CharField(max_length=30, blank=True)    # 专业
    facuty = models.CharField(max_length=30, blank=True)    # 所属院系
    graduate_year = models.SmallIntegerField()  # 毕业年限
    work_place = models.CharField(max_length=50)    # 工作地点
    industry = models.CharField(max_length=50, blank=True)  # 所属行业
    tel_number = models.CharField(max_length=15, blank=True)    # 联系电话
    net_contact = models.CharField(max_length=50, blank=True)   # 网络联系
    message = models.CharField(max_length=200, blank=True)  # 留言
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 用户

    def __str__(self):
        return self.name
