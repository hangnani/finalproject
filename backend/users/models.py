from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 用户扩展模型
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')
    phone = models.CharField(max_length=20, verbose_name='手机号')
    avatar = models.CharField(max_length=255, blank=True, null=True, verbose_name='头像URL')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return self.user.username
