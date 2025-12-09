from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework_simplejwt.tokens import RefreshToken

# 用户注册序列化器
class UserRegisterSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(max_length=20, required=True)
    phone = serializers.CharField(max_length=20, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email', 'first_name', 'last_name', 'student_id', 'phone']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("密码不匹配")
        return attrs

    def create(self, validated_data):
        # 创建用户
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()

        # 创建用户扩展信息
        UserProfile.objects.create(
            user=user,
            student_id=validated_data['student_id'],
            phone=validated_data['phone']
        )

        return user

# 用户登录序列化器
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = User.objects.filter(username=username).first()
            if not user or not user.check_password(password):
                raise serializers.ValidationError("用户名或密码错误")
        else:
            raise serializers.ValidationError("必须提供用户名和密码")

        attrs['user'] = user
        return attrs

# 用户信息序列化器
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    name = serializers.SerializerMethodField()
    is_admin = serializers.BooleanField(source='user.is_superuser')
    is_staff = serializers.BooleanField(source='user.is_staff')

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'name', 'student_id', 'phone', 'avatar', 'is_admin', 'is_staff']

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username

# User列表序列化器（用于管理员查看用户列表）
class UserListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    student_id = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    is_admin = serializers.BooleanField(source='is_superuser')
    is_staff = serializers.BooleanField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'student_id', 'phone', 'is_admin', 'is_staff']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username
    
    def get_student_id(self, obj):
        try:
            return obj.profile.student_id
        except UserProfile.DoesNotExist:
            return ''
    
    def get_phone(self, obj):
        try:
            return obj.profile.phone
        except UserProfile.DoesNotExist:
            return ''

# Token 序列化器
class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass