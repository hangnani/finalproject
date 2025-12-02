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