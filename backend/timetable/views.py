from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Course, Exam, Lecture, Activity, ReminderSetting, CourseReminder
from .serializers import (
    CourseSerializer, CourseCreateUpdateSerializer, CourseReminderUpdateSerializer,
    ExamSerializer, ExamCreateUpdateSerializer,
    LectureSerializer, LectureCreateUpdateSerializer,
    ActivitySerializer, ActivityCreateUpdateSerializer,
    ReminderSettingSerializer, ReminderSettingUpdateSerializer
)
from django.db.models import Q

# 课程视图集
class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CourseCreateUpdateSerializer
        return CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.filter(user=self.request.user)
        
        # 按星期几过滤
        day_of_week = self.request.query_params.get('day_of_week', None)
        if day_of_week:
            queryset = queryset.filter(day_of_week=day_of_week)
        
        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(teacher__icontains=search) | Q(location__icontains=search))
        
        # 排序
        queryset = queryset.order_by('day_of_week', 'start_time')
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 考试视图集
class ExamViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ExamCreateUpdateSerializer
        return ExamSerializer

    def get_queryset(self):
        user = self.request.user
        
        # 管理员可以查看所有考试，普通用户只能查看自己的考试
        if user.is_superuser or user.is_staff:
            queryset = Exam.objects.all()
        else:
            queryset = Exam.objects.filter(user=user)
        
        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(course__name__icontains=search) | Q(location__icontains=search))
        
        # 排序
        queryset = queryset.order_by('exam_date', 'start_time')
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 讲座视图集
class LectureViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LectureCreateUpdateSerializer
        return LectureSerializer

    def get_permissions(self):
        # 只有管理员可以创建、更新和删除讲座
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # 在这里可以添加管理员权限检查，例如检查用户是否属于管理员组
            # 为了简化，这里假设只有管理员可以创建、更新和删除讲座
            # 实际项目中应该使用权限系统，例如Django的Permission或自定义权限
            return [IsAuthenticated()]
        # 普通用户可以查看讲座
        return [IsAuthenticated()]

    def get_queryset(self):
        # 获取当前用户
        user = self.request.user
        
        # 公开讲座对所有用户可见，私有讲座只能被创建者查看
        queryset = Lecture.objects.filter(Q(is_public=True) | Q(created_by=user))
        
        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(speaker__icontains=search) | Q(location__icontains=search) | Q(description__icontains=search))
        
        # 排序
        queryset = queryset.order_by('lecture_date', 'start_time')
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# 活动视图集
class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ActivityCreateUpdateSerializer
        return ActivitySerializer

    def get_queryset(self):
        # 获取当前用户
        user = self.request.user
        
        # 公开活动对所有用户可见，私有活动只能被创建者查看
        queryset = Activity.objects.filter(Q(is_public=True) | Q(created_by=user))
        
        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(location__icontains=search) | Q(description__icontains=search))
        
        # 排序
        queryset = queryset.order_by('activity_date', 'start_time')
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# 提醒设置视图集
class ReminderSettingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ReminderSettingUpdateSerializer
        return ReminderSettingSerializer

    def get_queryset(self):
        return ReminderSetting.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 课程提醒更新视图
class CourseReminderUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseReminderUpdateSerializer

    def get_object(self):
        course_id = self.kwargs.get('course_id')
        try:
            course = Course.objects.get(id=course_id, user=self.request.user)
            return course.reminder
        except Course.DoesNotExist:
            self.permission_denied(self.request)

# 课程导入视图（简化版，实际项目中可能需要更复杂的 Excel 解析逻辑）
class CourseImportView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 这里简化处理，实际项目中应该解析 Excel 文件
        # 这里假设前端发送的是课程数据的 JSON 数组
        courses_data = request.data.get('courses', [])
        created_count = 0
        
        for course_data in courses_data:
            serializer = CourseCreateUpdateSerializer(data=course_data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                created_count += 1
        
        return Response({
            'message': f'成功导入 {created_count} 门课程',
            'count': created_count
        }, status=status.HTTP_201_CREATED)