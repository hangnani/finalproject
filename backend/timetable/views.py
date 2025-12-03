from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Course, CourseReminder
from .serializers import CourseSerializer, CourseCreateUpdateSerializer, CourseReminderUpdateSerializer
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