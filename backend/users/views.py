from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer, UserListSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# 用户注册视图
class UserRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # 生成 Token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "user": UserProfileSerializer(user.profile).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

# 用户登录视图
class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # 确保UserProfile存在
        from .models import UserProfile
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            # 创建默认的UserProfile
            profile = UserProfile.objects.create(
                user=user,
                student_id=f'{user.username}001',
                phone='13800138000'
            )
        
        # 生成 Token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "user": UserProfileSerializer(profile).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)

# 获取用户信息视图
class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.profile

# 修改密码视图
class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')
        
        if not old_password or not new_password or not new_password_confirm:
            return Response({"error": "必须提供旧密码和新密码"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(old_password):
            return Response({"error": "旧密码错误"}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != new_password_confirm:
            return Response({"error": "新密码不匹配"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({"message": "密码修改成功"}, status=status.HTTP_200_OK)

# 用户视图集，用于获取所有用户（管理员专用）
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    http_method_names = ['get']  # 只允许GET请求
    
    def get_queryset(self):
        # 只有管理员可以查看所有用户
        return User.objects.all()