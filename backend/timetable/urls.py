from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, CourseReminderUpdateView, CourseImportView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:course_id>/reminder/', CourseReminderUpdateView.as_view(), name='course-reminder-update'),
    path('courses/import/', CourseImportView.as_view(), name='course-import'),
]