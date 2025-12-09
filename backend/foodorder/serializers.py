from rest_framework import serializers
from django.db.models import Avg
from .models import Restaurant, Dish, CartItem, Order, OrderItem, OrderReview, OrderStatusHistory, DishReview
from users.serializers import UserProfileSerializer

# 餐厅序列化器
class RestaurantSerializer(serializers.ModelSerializer):
    dish_count = serializers.IntegerField(source='dishes.count', read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'location', 'opening_hours', 'created_at', 'updated_at', 'dish_count']

# 菜品序列化器
class DishSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True, default=0)
    review_count = serializers.IntegerField(source='reviews.count', read_only=True, default=0)

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(avg=Avg('rating'))['avg']
        return float(avg) if avg else 0.0

    class Meta:
        model = Dish
        fields = ['id', 'restaurant', 'name', 'description', 'price', 'image', 'status', 'created_at', 'updated_at', 'average_rating', 'review_count']

# 购物车项序列化器
class CartItemSerializer(serializers.ModelSerializer):
    dish = DishSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'dish', 'quantity', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_total_price(self, obj):
        return obj.dish.price * obj.quantity

# 购物车项创建/更新序列化器
class CartItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['dish', 'quantity']

    def create(self, validated_data):
        user = self.context['request'].user
        dish = validated_data['dish']
        quantity = validated_data['quantity']

        # 检查购物车中是否已存在该菜品
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            dish=dish,
            defaults={'quantity': quantity}
        )

        # 如果已存在，则更新数量
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item

# 订单详情序列化器
class OrderItemSerializer(serializers.ModelSerializer):
    dish = DishSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'dish', 'quantity', 'price']

# 订单评价序列化器
class OrderReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderReview
        fields = ['id', 'rating', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

# 订单状态历史序列化器
class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'status', 'status_display', 'change_time', 'reason', 'created_by']
        read_only_fields = ['id', 'change_time']

# 菜品评价序列化器
class DishReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = DishReview
        fields = ['id', 'user', 'dish', 'rating', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

# 菜品评价创建序列化器
class DishReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishReview
        fields = ['dish', 'rating', 'content']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        # 自动设置当前用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

# 订单序列化器
class OrderSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    review = OrderReviewSerializer(read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'total_price', 'status', 'status_display', 'payment_method', 'payment_method_display', 'delivery_address', 'created_at', 'updated_at', 'items', 'review', 'status_history']
        read_only_fields = ['user', 'total_price', 'status', 'created_at', 'updated_at']

# 订单创建序列化器
class OrderCreateSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.IntegerField(required=True)
    delivery_address = serializers.CharField(required=True)
    payment_method = serializers.IntegerField(required=True)

    class Meta:
        model = Order
        fields = ['restaurant_id', 'delivery_address', 'payment_method']

    def validate_restaurant_id(self, value):
        try:
            Restaurant.objects.get(id=value)
            return value
        except Restaurant.DoesNotExist:
            raise serializers.ValidationError("餐厅不存在")

    def create(self, validated_data):
        user = self.context['request'].user
        restaurant_id = validated_data['restaurant_id']
        delivery_address = validated_data['delivery_address']
        payment_method = validated_data['payment_method']

        # 获取用户购物车中该餐厅的菜品
        cart_items = CartItem.objects.filter(user=user, dish__restaurant_id=restaurant_id)
        if not cart_items.exists():
            raise serializers.ValidationError("购物车中没有该餐厅的菜品")

        # 计算订单总价
        total_price = sum(item.dish.price * item.quantity for item in cart_items)

        # 创建订单
        order = Order.objects.create(
            user=user,
            restaurant_id=restaurant_id,
            total_price=total_price,
            status=1,  # 假设创建即已支付
            payment_method=payment_method,
            delivery_address=delivery_address
        )

        # 创建订单详情
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                dish=cart_item.dish,
                quantity=cart_item.quantity,
                price=cart_item.dish.price
            )

        # 清空购物车中该餐厅的菜品
        cart_items.delete()

        return order