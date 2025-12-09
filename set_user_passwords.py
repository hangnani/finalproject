#!/usr/bin/env python3
"""
设置用户密码的脚本
"""

import os
import sys

# 添加backend目录到Python路径
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')

# 初始化Django
import django
django.setup()

from django.contrib.auth.models import User


def set_user_passwords():
    """设置所有用户的密码"""
    try:
        # 用户密码映射
        user_passwords = {
            'admin': 'admin123',
            'yang': '20020409',
            'test': 'test123',
            'testuser': 'test123'
        }
        
        print("设置用户密码：")
        print("-" * 30)
        
        for username, password in user_passwords.items():
            try:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                print(f"✓ {username}: {password}")
            except User.DoesNotExist:
                print(f"✗ {username}: 用户不存在")
        
        print("-" * 30)
        print("密码设置完成！")
        return True
    except Exception as e:
        print(f"设置密码失败: {e}")
        return False


if __name__ == '__main__':
    set_user_passwords()