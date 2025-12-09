from rest_framework import serializers
from .models import Product, Category, ProductFavorite, ProductComment, Transaction, TransactionReview
from users.serializers import UserProfileSerializer

# 商品分类序列化器
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']

# 商品序列化器
class ProductSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(source='user.profile', read_only=True)
    category = CategorySerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    favorite_count = serializers.IntegerField(source='favorited_by.count', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'user', 'name', 'description', 'price', 'category', 'status', 'images', 'contact', 'created_at', 'updated_at', 'is_favorited', 'comment_count', 'favorite_count']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by.filter(user=request.user).exists()
        return False

# 商品创建/更新序列化器
class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'status', 'images', 'contact']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

# 商品收藏序列化器
class ProductFavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductFavorite
        fields = ['id', 'product', 'created_at']

# 商品留言序列化器
class ProductCommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = ProductComment
        fields = ['id', 'user', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

# 交易记录序列化器
class TransactionSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    buyer = UserProfileSerializer(read_only=True)
    seller = UserProfileSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'product', 'buyer', 'seller', 'status', 'status_display', 'transaction_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'buyer', 'seller', 'created_at', 'updated_at']

# 交易记录创建序列化器
class TransactionCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=True)
    
    class Meta:
        model = Transaction
        fields = ['product_id', 'transaction_price']
    
    def create(self, validated_data):
        # 获取当前用户（买家）
        buyer = self.context['request'].user
        # 获取商品
        product = Product.objects.get(id=validated_data['product_id'])
        # 获取卖家
        seller = product.user
        # 创建交易记录
        transaction = Transaction.objects.create(
            product=product,
            buyer=buyer,
            seller=seller,
            transaction_price=validated_data['transaction_price']
        )
        # 更新商品状态为已售出
        product.status = 1
        product.save()
        return transaction

# 交易评价序列化器
class TransactionReviewSerializer(serializers.ModelSerializer):
    reviewer = UserProfileSerializer(read_only=True)
    reviewed = UserProfileSerializer(read_only=True)
    review_type_display = serializers.CharField(source='get_review_type_display', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    
    class Meta:
        model = TransactionReview
        fields = ['id', 'transaction', 'reviewer', 'reviewed', 'review_type', 'review_type_display', 'content', 'rating', 'created_at']
        read_only_fields = ['id', 'reviewer', 'reviewed', 'created_at']

# 交易评价创建序列化器
class TransactionReviewCreateSerializer(serializers.ModelSerializer):
    transaction_id = serializers.IntegerField(required=True)
    review_type = serializers.IntegerField(required=True)
    
    class Meta:
        model = TransactionReview
        fields = ['transaction_id', 'review_type', 'content', 'rating']
    
    def create(self, validated_data):
        # 获取当前用户（评价者）
        reviewer = self.context['request'].user
        # 获取交易
        transaction = Transaction.objects.get(id=validated_data['transaction_id'])
        # 确定被评价者
        review_type = validated_data['review_type']
        reviewed = transaction.seller if review_type == 0 else transaction.buyer
        # 创建交易评价
        return TransactionReview.objects.create(
            transaction=transaction,
            reviewer=reviewer,
            reviewed=reviewed,
            content=validated_data['content'],
            rating=validated_data['rating'],
            review_type=review_type
        )