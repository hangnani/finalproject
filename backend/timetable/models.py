from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 课程模型
class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', verbose_name='所属用户')
    name = models.CharField(max_length=100, verbose_name='课程名称')
    teacher = models.CharField(max_length=50, verbose_name='教师姓名')
    day_of_week = models.IntegerField(verbose_name='星期几（1-7）')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    location = models.CharField(max_length=100, verbose_name='上课地点')
    credit = models.FloatField(verbose_name='学分')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程'
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return self.name

# 课程提醒模型
class CourseReminder(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='reminder', verbose_name='课程')
    is_enabled = models.BooleanField(default=True, verbose_name='是否启用')
    reminder_minutes = models.IntegerField(default=10, verbose_name='提前提醒分钟数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '课程提醒'
        verbose_name_plural = '课程提醒'

    def __str__(self):
        return f'{self.course.name} 的提醒设置'