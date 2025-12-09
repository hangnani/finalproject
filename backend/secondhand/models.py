from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 商品分类
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'

    def __str__(self):
        return self.name

# 商品模型
class Product(models.Model):
    STATUS_CHOICES = (
        (0, '在售'),
        (1, '已售出'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name='发布者')
    name = models.CharField(max_length=100, verbose_name='商品名称')
    description = models.TextField(verbose_name='商品描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name='商品分类')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='商品状态')
    images = models.JSONField(default=list, blank=True, verbose_name='商品图片URL列表')
    contact = models.CharField(max_length=100, verbose_name='联系方式')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '二手商品'
        verbose_name_plural = '二手商品'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

# 商品收藏
class ProductFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_products', verbose_name='用户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='商品')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        verbose_name = '商品收藏'
        verbose_name_plural = '商品收藏'
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} 收藏了 {self.product.name}'

# 商品留言
class ProductComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_comments', verbose_name='留言用户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='商品')
    content = models.TextField(verbose_name='留言内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='留言时间')

    class Meta:
        verbose_name = '商品留言'
        verbose_name_plural = '商品留言'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.user.username} 在 {self.product.name} 下留言'

# 交易记录模型
class Transaction(models.Model):
    # 交易相关的商品
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions', verbose_name='交易商品')
    # 买家和卖家
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_transactions', verbose_name='买家')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_transactions', verbose_name='卖家')
    # 交易状态
    STATUS_CHOICES = (
        (0, '待确认'),
        (1, '已确认'),
        (2, '已完成'),
        (3, '已取消'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='交易状态')
    # 交易价格（允许与商品价格不同，比如议价）
    transaction_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='交易价格')
    # 交易创建和更新时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '交易记录'
        verbose_name_plural = '交易记录'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.buyer.username} 购买 {self.product.name} 的交易记录'

# 交易评价模型
class TransactionReview(models.Model):
    # 所属交易
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='reviews', verbose_name='所属交易')
    # 评价者
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews', verbose_name='评价者')
    # 被评价者
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews', verbose_name='被评价者')
    # 评价类型（买家评价卖家或卖家评价买家）
    REVIEW_TYPE_CHOICES = (
        (0, '买家评价卖家'),
        (1, '卖家评价买家'),
    )
    review_type = models.IntegerField(choices=REVIEW_TYPE_CHOICES, verbose_name='评价类型')
    # 评价内容
    content = models.TextField(blank=True, verbose_name='评价内容')
    # 评分（1-5星）
    rating = models.IntegerField(verbose_name='评分（1-5）')
    # 评价创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评价时间')

    class Meta:
        verbose_name = '交易评价'
        verbose_name_plural = '交易评价'
        ordering = ['-created_at']
        # 确保每个交易中每个用户只能评价一次
        unique_together = ('transaction', 'reviewer', 'reviewed')

    def __str__(self):
        return f'{self.reviewer.username} 对 {self.reviewed.username} 的评价'