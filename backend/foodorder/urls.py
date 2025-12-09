from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RestaurantViewSet, DishViewSet, CartViewSet, 
    CartItemDeleteView, OrderViewSet, OrderCreateView,
    OrderCancelView, OrderReviewView, OrderStatusUpdateView, DishReviewViewSet
)

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'dishes', DishViewSet, basename='dish')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'dish-reviews', DishReviewViewSet, basename='dish-review')

urlpatterns = [
    path('', include(router.urls)),
    path('cart/<int:cart_item_id>/delete/', CartItemDeleteView.as_view(), name='cart-item-delete'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:order_id>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
    path('orders/<int:order_id>/review/', OrderReviewView.as_view(), name='order-review'),
    path('orders/<int:order_id>/status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
]