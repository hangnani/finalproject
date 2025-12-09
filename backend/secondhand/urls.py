from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CategoryViewSet, ProductFavoriteView, 
    MyFavoriteProductsView, ProductCommentView, TransactionViewSet,
    TransactionReviewViewSet
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'reviews', TransactionReviewViewSet, basename='transaction-review')

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:product_id>/favorite/', ProductFavoriteView.as_view(), name='product-favorite'),
    path('products/favorites/', MyFavoriteProductsView.as_view(), name='my-favorite-products'),
    path('products/<int:product_id>/comments/', ProductCommentView.as_view(), name='product-comments'),
]