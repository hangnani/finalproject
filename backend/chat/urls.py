from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet, MarkMessagesAsReadView

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# 消息路由（嵌套在对话下）
conversation_router = DefaultRouter()
conversation_router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    # 对话相关的消息路由
    path('conversations/<int:conversation_id>/', include(conversation_router.urls)),
    # 标记消息为已读
    path('conversations/<int:conversation_id>/mark-as-read/', MarkMessagesAsReadView.as_view(), name='mark-as-read'),
]