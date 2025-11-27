from rest_framework import serializers
from .models import Product, Category, ProductFavorite, ProductComment
from users.serializers import UserProfileSerializer

# 商品分类序列化器
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']

# 商品序列化器
class ProductSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
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