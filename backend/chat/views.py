from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer, ConversationCreateSerializer,
    MessageSerializer, MessageCreateSerializer
)
from django.db.models import Q

# 对话视图集
class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_serializer_class(self):
        # 创建操作返回完整的对话信息
        if self.action in ['update', 'partial_update']:
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        # 获取当前用户
        user = self.request.user
        # 查询当前用户参与的所有对话
        queryset = Conversation.objects.filter(Q(buyer=user) | Q(seller=user))
        # 按更新时间倒序排序
        queryset = queryset.order_by('-updated_at')
        return queryset

    def create(self, request, *args, **kwargs):
        # 使用创建序列化器验证数据
        create_serializer = ConversationCreateSerializer(data=request.data, context={'request': request})
        create_serializer.is_valid(raise_exception=True)
        
        # 保存对话
        conversation = create_serializer.save(buyer=request.user)
        
        # 使用完整序列化器返回响应
        serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

# 消息视图集
class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MessageCreateSerializer
        return MessageSerializer

    def get_queryset(self):
        # 获取对话ID
        conversation_id = self.kwargs.get('conversation_id')
        # 查询该对话的所有消息
        queryset = Message.objects.filter(conversation_id=conversation_id)
        # 按创建时间排序
        queryset = queryset.order_by('created_at')
        return queryset

    def list(self, request, *args, **kwargs):
        # 获取对话ID
        conversation_id = self.kwargs.get('conversation_id')
        # 查询该对话的所有消息
        queryset = self.get_queryset()
        # 将当前用户的未读消息标记为已读
        queryset.filter(receiver=request.user, status=0).update(status=1)
        # 更新对话的未读消息数
        conversation = Conversation.objects.get(id=conversation_id)
        conversation.unread_count = 0
        conversation.save()
        # 序列化消息
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

# 标记消息为已读视图
class MarkMessagesAsReadView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # 获取对话ID
        conversation_id = self.kwargs.get('conversation_id')
        # 获取当前用户
        user = request.user
        # 标记该对话中当前用户的所有未读消息为已读
        updated_count = Message.objects.filter(
            conversation_id=conversation_id,
            receiver=user,
            status=0
        ).update(status=1)
        # 更新对话的未读消息数
        conversation = Conversation.objects.get(id=conversation_id)
        conversation.unread_count = 0
        conversation.save()
        return Response(
            {'message': f'已标记 {updated_count} 条消息为已读'}, 
            status=status.HTTP_200_OK
        )