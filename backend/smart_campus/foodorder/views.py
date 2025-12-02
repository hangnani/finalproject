from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Restaurant, Dish, CartItem, Order, OrderReview
from .serializers import (
    RestaurantSerializer, DishSerializer, CartItemSerializer, 
    CartItemCreateUpdateSerializer, OrderSerializer, OrderCreateSerializer,
    OrderReviewSerializer
)
from django.db.models import Q

# 餐厅视图集
class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]

# 菜品视图集
class DishViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 按餐厅过滤
        restaurant_id = self.request.query_params.get('restaurant', None)
        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        
        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        
        # 按状态过滤
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset

# 购物车视图集
class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CartItemCreateUpdateSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 购物车项删除视图
class CartItemDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart_item_id = self.kwargs.get('cart_item_id')
        try:
            return CartItem.objects.get(id=cart_item_id, user=self.request.user)
        except CartItem.DoesNotExist:
            self.permission_denied(self.request)

# 订单视图集
class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        
        # 按状态过滤
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # 按餐厅过滤
        restaurant_id = self.request.query_params.get('restaurant', None)
        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        
        # 排序
        queryset = queryset.order_by('-created_at')
        
        return queryset

# 订单创建视图
class OrderCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

# 订单取消视图
class OrderCancelView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_object(self):
        order_id = self.kwargs.get('order_id')
        try:
            return Order.objects.get(id=order_id, user=self.request.user)
        except Order.DoesNotExist:
            self.permission_denied(self.request)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        # 只有待支付和已支付状态的订单可以取消
        if order.status in [0, 1]:
            order.status = 5  # 已取消
            order.save()
            return Response(self.get_serializer(order).data)
        return Response({"error": "该订单状态不允许取消"}, status=status.HTTP_400_BAD_REQUEST)

# 订单评价视图
class OrderReviewView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderReviewSerializer

    def create(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        try:
            order = Order.objects.get(id=order_id, user=self.request.user, status=4)  # 只有已完成的订单可以评价
        except Order.DoesNotExist:
            return Response({"error": "该订单不存在或状态不允许评价"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查是否已经评价过
        if hasattr(order, 'review'):
            return Response({"error": "该订单已经评价过"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(order=order)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)