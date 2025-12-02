#!/usr/bin/env python
"""
创建默认用户脚本
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 配置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
import django
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from users.models import UserProfile

def create_default_users():
    """创建默认用户"""
    # 创建或更新管理员用户
    print("正在创建/更新管理员用户...")
    admin_user, created = User.objects.update_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': '管理员',
            'is_staff': True,
            'is_superuser': True,
            'password': make_password('password123')
        }
    )
    
    # 创建或更新管理员用户资料
    UserProfile.objects.update_or_create(
        user=admin_user,
        defaults={
            'student_id': 'admin001',
            'phone': '13800138000'
        }
    )
    
    # 创建或更新多个普通用户
    print("正在创建/更新多个普通用户...")
    for i in range(1, 21):
        username = f'user{i}'
        normal_user, created = User.objects.update_or_create(
            username=username,
            defaults={
                'email': f'{username}@example.com',
                'first_name': f'用户',
                'last_name': f'{i}',
                'is_staff': False,
                'is_superuser': False,
                'password': make_password('password123')
            }
        )
        
        # 创建或更新普通用户资料
        UserProfile.objects.update_or_create(
            user=normal_user,
            defaults={
                'student_id': f'{username}_{i:03d}',
                'phone': f'13800138{i:03d}'
            }
        )
    
    print("默认用户创建/更新成功！")
    print("管理员账号：admin / password123")
    print("普通用户账号：user1-user20 / password123")

if __name__ == '__main__':
    create_default_users()