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

# 考试模型
class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams', verbose_name='所属用户')
    name = models.CharField(max_length=100, verbose_name='考试名称')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams', verbose_name='关联课程')
    exam_date = models.DateField(verbose_name='考试日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    location = models.CharField(max_length=100, verbose_name='考试地点')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '考试'
        verbose_name_plural = '考试'
        ordering = ['exam_date', 'start_time']

    def __str__(self):
        return f'{self.course.name} - {self.name}'

# 讲座模型
class Lecture(models.Model):
    title = models.CharField(max_length=150, verbose_name='讲座标题')
    speaker = models.CharField(max_length=100, verbose_name='主讲人')
    lecture_date = models.DateField(verbose_name='讲座日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    location = models.CharField(max_length=100, verbose_name='讲座地点')
    description = models.TextField(verbose_name='讲座描述')
    is_public = models.BooleanField(default=True, verbose_name='是否公开')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lectures', verbose_name='创建者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '讲座'
        verbose_name_plural = '讲座'
        ordering = ['lecture_date', 'start_time']

    def __str__(self):
        return self.title

# 活动模型
class Activity(models.Model):
    title = models.CharField(max_length=150, verbose_name='活动标题')
    activity_date = models.DateField(verbose_name='活动日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    location = models.CharField(max_length=100, verbose_name='活动地点')
    description = models.TextField(verbose_name='活动描述')
    is_public = models.BooleanField(default=True, verbose_name='是否公开')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities', verbose_name='创建者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '活动'
        verbose_name_plural = '活动'
        ordering = ['activity_date', 'start_time']

    def __str__(self):
        return self.title

# 提醒设置模型
class ReminderSetting(models.Model):
    TYPE_CHOICES = (
        ('course', '课程'),
        ('exam', '考试'),
        ('lecture', '讲座'),
        ('activity', '活动'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminder_settings', verbose_name='所属用户')
    reminder_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='提醒类型')
    is_enabled = models.BooleanField(default=True, verbose_name='是否启用')
    reminder_minutes = models.IntegerField(default=60, verbose_name='提前提醒分钟数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '提醒设置'
        verbose_name_plural = '提醒设置'
        unique_together = ('user', 'reminder_type')

    def __str__(self):
        return f'{self.user.username} 的{self.get_reminder_type_display()}提醒设置'

# 课程提醒模型（保留以兼容现有功能）
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