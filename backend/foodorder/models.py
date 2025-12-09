from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# 餐厅模型
class Restaurant(models.Model):
    name = models.CharField(max_length=100, verbose_name='餐厅名称')
    description = models.TextField(blank=True, verbose_name='餐厅描述')
    location = models.CharField(max_length=100, verbose_name='餐厅位置')
    opening_hours = models.CharField(max_length=100, verbose_name='营业时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '餐厅'
        verbose_name_plural = '餐厅'

    def __str__(self):
        return self.name

# 菜品模型
class Dish(models.Model):
    STATUS_CHOICES = (
        (0, '在售'),
        (1, '售罄'),
    )

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='dishes', verbose_name='所属餐厅')
    name = models.CharField(max_length=100, verbose_name='菜品名称')
    description = models.TextField(blank=True, verbose_name='菜品描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='菜品价格')
    image = models.CharField(max_length=255, blank=True, null=True, verbose_name='菜品图片URL')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='菜品状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '菜品'
        verbose_name_plural = '菜品'

    def __str__(self):
        return self.name

# 购物车模型
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', verbose_name='用户')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='cart_items', verbose_name='菜品')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '购物车项'
        verbose_name_plural = '购物车项'
        unique_together = ('user', 'dish')

    def __str__(self):
        return f'{self.user.username} 的购物车：{self.dish.name} x {self.quantity}'

# 订单模型
class Order(models.Model):
    STATUS_CHOICES = (
        (0, '待支付'),
        (1, '已支付'),
        (2, '已接单'),
        (3, '配送中'),
        (4, '已完成'),
        (5, '已取消'),
    )

    PAYMENT_METHOD_CHOICES = (
        (0, '微信支付'),
        (1, '支付宝'),
        (2, '校园卡'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='用户')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders', verbose_name='餐厅')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总价')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='订单状态')
    payment_method = models.IntegerField(choices=PAYMENT_METHOD_CHOICES, default=0, verbose_name='支付方式')
    delivery_address = models.CharField(max_length=255, verbose_name='配送地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']

    def __str__(self):
        return f'订单 {self.id} - {self.get_status_display()}'

# 订单详情模型
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='order_items', verbose_name='菜品')
    quantity = models.IntegerField(verbose_name='数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='菜品单价')

    class Meta:
        verbose_name = '订单详情'
        verbose_name_plural = '订单详情'

    def __str__(self):
        return f'{self.order.id} - {self.dish.name} x {self.quantity}'

# 订单评价模型
class OrderReview(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review', verbose_name='订单')
    rating = models.IntegerField(verbose_name='评分（1-5）')
    content = models.TextField(blank=True, verbose_name='评价内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '订单评价'
        verbose_name_plural = '订单评价'

    def __str__(self):
        return f'订单 {self.order.id} 的评价'

# 订单状态历史模型
class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history', verbose_name='订单')
    status = models.IntegerField(choices=Order.STATUS_CHOICES, verbose_name='状态')
    status_display = models.CharField(max_length=50, verbose_name='状态名称')
    change_time = models.DateTimeField(auto_now_add=True, verbose_name='变更时间')
    reason = models.TextField(blank=True, verbose_name='变更原因')
    created_by = models.CharField(max_length=100, blank=True, verbose_name='操作人')

    class Meta:
        verbose_name = '订单状态历史'
        verbose_name_plural = '订单状态历史'
        ordering = ['change_time']

    def __str__(self):
        return f'订单 {self.order.id} - {self.status_display} ({self.change_time})'

    def save(self, *args, **kwargs):
        # 自动设置状态名称
        self.status_display = dict(Order.STATUS_CHOICES)[self.status]
        super().save(*args, **kwargs)

# 订单状态变化信号处理函数
@receiver(post_save, sender=Order)
def create_order_status_history(sender, instance, created, **kwargs):
    if created:
        # 订单创建时，记录初始状态
        OrderStatusHistory.objects.create(
            order=instance,
            status=instance.status,
            status_display=instance.get_status_display(),
            reason='订单创建',
            created_by=instance.user.username
        )
    else:
        # 订单更新时，检查状态是否变化
        try:
            old_instance = Order.objects.get(id=instance.id)
            if old_instance.status != instance.status:
                # 状态变化，记录历史
                OrderStatusHistory.objects.create(
                    order=instance,
                    status=instance.status,
                    status_display=instance.get_status_display(),
                    reason='状态更新',
                    created_by='系统'
                )
        except Order.DoesNotExist:
            pass

# 菜品评价模型
class DishReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dish_reviews', verbose_name='评价用户')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='reviews', verbose_name='评价菜品')
    rating = models.IntegerField(verbose_name='评分（1-5）')
    content = models.TextField(blank=True, verbose_name='评价内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评价时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '菜品评价'
        verbose_name_plural = '菜品评价'
        ordering = ['-created_at']
        unique_together = ('user', 'dish')

    def __str__(self):
        return f'{self.user.username} 对 {self.dish.name} 的评价'