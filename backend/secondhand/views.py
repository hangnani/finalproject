from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, Category, ProductFavorite, ProductComment
from .serializers import ProductSerializer, ProductCreateUpdateSerializer, CategorySerializer, ProductFavoriteSerializer, ProductCommentSerializer
from django.db.models import Q

# 商品分类视图集
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

# 商品视图集
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        
        # 分类过滤
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # 价格范围过滤
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # 状态过滤
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # 排序
        sort = self.request.query_params.get('sort', '-created_at')
        queryset = queryset.order_by(sort)
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 商品收藏视图
class ProductFavoriteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductFavoriteSerializer

    def post(self, request, product_id):
        # 检查商品是否存在
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "商品不存在"}, status=status.HTTP_404_NOT_FOUND)
        
        # 检查是否已经收藏
        if ProductFavorite.objects.filter(user=request.user, product=product).exists():
            return Response({"error": "已经收藏过该商品"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建收藏
        favorite = ProductFavorite.objects.create(user=request.user, product=product)
        return Response(self.get_serializer(favorite).data, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        # 检查商品是否存在
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "商品不存在"}, status=status.HTTP_404_NOT_FOUND)
        
        # 删除收藏
        deleted, _ = ProductFavorite.objects.filter(user=request.user, product=product).delete()
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "未收藏该商品"}, status=status.HTTP_400_BAD_REQUEST)

# 我的收藏列表视图
class MyFavoriteProductsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(favorited_by__user=self.request.user)

# 商品留言视图
class ProductCommentView(generics.ListCreateAPIView):
    serializer_class = ProductCommentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return ProductComment.objects.filter(product_id=product_id).order_by('created_at')

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        serializer.save(product_id=product_id, user=self.request.user)