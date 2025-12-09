import os
import sys
import django

# 获取当前脚本的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 获取backend目录
backend_dir = os.path.join(script_dir, 'backend')
# 添加backend目录到Python路径
sys.path.insert(0, backend_dir)

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile

# 检查用户是否存在
user, created = User.objects.get_or_create(
    username='yang',
    defaults={
        'email': 'yang@example.com',
        'first_name': '杨',
        'last_name': '同学',
        'is_staff': False,
        'is_superuser': False
    }
)

# 设置密码
user.set_password('yang123')
user.save()

# 检查是否有UserProfile
if not hasattr(user, 'profile'):
    # 创建UserProfile
    UserProfile.objects.create(
        user=user,
        student_id='20240001',
        phone='13800138000'
    )

print(f'用户"yang"处理完成:')
print(f'- 存在: {not created}')
print(f'- 用户名: {user.username}')
print(f'- 邮箱: {user.email}')
print(f'- 姓名: {user.first_name} {user.last_name}')
print(f'- 是否管理员: {user.is_superuser}')
print(f'- 学生ID: {user.profile.student_id}')
print(f'- 手机号: {user.profile.phone}')
