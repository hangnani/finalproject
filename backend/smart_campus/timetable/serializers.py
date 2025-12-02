from rest_framework import serializers
from .models import Course, CourseReminder

# 课程提醒序列化器
class CourseReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReminder
        fields = ['id', 'is_enabled', 'reminder_minutes', 'created_at', 'updated_at']

# 课程序列化器
class CourseSerializer(serializers.ModelSerializer):
    reminder = CourseReminderSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'teacher', 'day_of_week', 'start_time', 'end_time', 'location', 'credit', 'created_at', 'updated_at', 'reminder']
        read_only_fields = ['created_at', 'updated_at']

# 课程创建/更新序列化器
class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'teacher', 'day_of_week', 'start_time', 'end_time', 'location', 'credit']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        course = super().create(validated_data)
        # 自动创建课程提醒
        CourseReminder.objects.create(course=course)
        return course

# 课程提醒更新序列化器
class CourseReminderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReminder
        fields = ['is_enabled', 'reminder_minutes']