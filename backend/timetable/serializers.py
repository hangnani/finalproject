from rest_framework import serializers
from .models import Course, Exam, Lecture, Activity, ReminderSetting, CourseReminder

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

# 考试序列化器
class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'name', 'course', 'exam_date', 'start_time', 'end_time', 'location', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

# 考试创建/更新序列化器
class ExamCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['name', 'course', 'exam_date', 'start_time', 'end_time', 'location']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

# 讲座序列化器
class LectureSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    
    class Meta:
        model = Lecture
        fields = ['id', 'title', 'speaker', 'lecture_date', 'start_time', 'end_time', 'location', 'description', 'is_public', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'created_by']

# 讲座创建/更新序列化器
class LectureCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['title', 'speaker', 'lecture_date', 'start_time', 'end_time', 'location', 'description', 'is_public']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

# 活动序列化器
class ActivitySerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    
    class Meta:
        model = Activity
        fields = ['id', 'title', 'activity_date', 'start_time', 'end_time', 'location', 'description', 'is_public', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'created_by']

# 活动创建/更新序列化器
class ActivityCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['title', 'activity_date', 'start_time', 'end_time', 'location', 'description', 'is_public']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

# 提醒设置序列化器
class ReminderSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReminderSetting
        fields = ['id', 'reminder_type', 'is_enabled', 'reminder_minutes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'user']

# 提醒设置更新序列化器
class ReminderSettingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReminderSetting
        fields = ['is_enabled', 'reminder_minutes']