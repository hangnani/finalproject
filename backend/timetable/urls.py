from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, CourseReminderUpdateView, CourseImportView,
    ExamViewSet, LectureViewSet, ActivityViewSet, ReminderSettingViewSet
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'lectures', LectureViewSet, basename='lecture')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'reminder-settings', ReminderSettingViewSet, basename='reminder-setting')

urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:course_id>/reminder/', CourseReminderUpdateView.as_view(), name='course-reminder-update'),
    path('courses/import/', CourseImportView.as_view(), name='course-import'),
]