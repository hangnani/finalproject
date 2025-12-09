from rest_framework import serializers
from .models import Conversation, Message
from users.serializers import UserProfileSerializer
from secondhand.serializers import ProductSerializer

# 消息序列化器
class MessageSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer(source='sender.profile', read_only=True)
    receiver = UserProfileSerializer(source='receiver.profile', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'receiver', 'content', 'message_type', 'status', 'created_at']
        read_only_fields = ['id', 'sender', 'receiver', 'created_at']

# 消息创建序列化器
class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'message_type']
        read_only_fields = ['id', 'sender', 'receiver', 'conversation', 'status', 'created_at']

    def create(self, validated_data):
        # 获取当前用户（发送者）
        sender = self.context['request'].user
        # 获取对话ID
        conversation_id = self.context['view'].kwargs.get('conversation_id')
        # 获取对话
        conversation = Conversation.objects.get(id=conversation_id)
        # 确定接收者
        receiver = conversation.buyer if sender == conversation.seller else conversation.seller
        # 创建消息
        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            receiver=receiver,
            **validated_data
        )
        # 更新对话的最后一条消息
        conversation.last_message = message.content[:50] + '...' if len(message.content) > 50 else message.content
        conversation.unread_count += 1
        conversation.save()
        return message

# 对话序列化器
class ConversationSerializer(serializers.ModelSerializer):
    buyer = UserProfileSerializer(source='buyer.profile', read_only=True)
    seller = UserProfileSerializer(source='seller.profile', read_only=True)
    product = ProductSerializer(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    # 当前用户未读消息数
    user_unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'buyer', 'seller', 'product', 'status', 'created_at', 'updated_at', 'last_message', 'unread_count', 'user_unread_count', 'messages']
        read_only_fields = ['id', 'buyer', 'seller', 'product', 'created_at', 'updated_at', 'last_message', 'unread_count']
    
    def get_user_unread_count(self, obj):
        # 获取当前用户
        user = self.context['request'].user
        # 返回当前用户的未读消息数
        return obj.messages.filter(receiver=user, status=0).count()

# 对话创建序列化器
class ConversationCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=True)
    seller_id = serializers.IntegerField(required=True)
    
    class Meta:
        model = Conversation
        fields = ['product_id', 'seller_id']
    
    def create(self, validated_data):
        # 获取当前用户（买家）
        buyer = self.context['request'].user
        # 获取商品和卖家
        product_id = validated_data['product_id']
        seller_id = validated_data['seller_id']
        
        # 检查是否已存在对话
        existing_conversation = Conversation.objects.filter(
            buyer=buyer,
            seller_id=seller_id,
            product_id=product_id
        ).first()
        
        if existing_conversation:
            # 如果已存在，返回现有对话
            return existing_conversation
        
        # 创建新对话
        conversation = Conversation.objects.create(
            buyer=buyer,
            seller_id=seller_id,
            product_id=product_id
        )
        
        return conversation