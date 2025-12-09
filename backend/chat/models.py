from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 对话模型
class Conversation(models.Model):
    # 对话参与者
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_conversations', verbose_name='买家')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_conversations', verbose_name='卖家')
    # 关联的商品
    product = models.ForeignKey('secondhand.Product', on_delete=models.CASCADE, related_name='conversations', verbose_name='关联商品')
    # 对话状态
    STATUS_CHOICES = (
        (0, '进行中'),
        (1, '已结束'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='对话状态')
    # 对话创建和更新时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 最后一条消息
    last_message = models.CharField(max_length=255, blank=True, verbose_name='最后一条消息')
    # 未读消息计数
    unread_count = models.IntegerField(default=0, verbose_name='未读消息数')

    class Meta:
        verbose_name = '对话'
        verbose_name_plural = '对话'
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.buyer.username} 与 {self.seller.username} 的对话'

# 消息模型
class Message(models.Model):
    # 所属对话
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', verbose_name='所属对话')
    # 发送者
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='发送者')
    # 接收者
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name='接收者')
    # 消息内容
    content = models.TextField(verbose_name='消息内容')
    # 消息类型
    MESSAGE_TYPE_CHOICES = (
        (0, '文本'),
        (1, '图片'),
        (2, '文件'),
    )
    message_type = models.IntegerField(choices=MESSAGE_TYPE_CHOICES, default=0, verbose_name='消息类型')
    # 消息状态
    STATUS_CHOICES = (
        (0, '未读'),
        (1, '已读'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='消息状态')
    # 消息创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = '消息'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender.username} 发送给 {self.receiver.username} 的消息'