#!/usr/bin/env python3
"""
获取所有用户账号信息的脚本
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


def get_all_users():
    """获取所有用户账号信息"""
    try:
        users = User.objects.all()
        user_list = []
        
        print("所有用户账号信息：")
        print("-" * 30)
        
        for user in users:
            print(f"用户名: {user.username}")
            user_list.append(user.username)
        
        print("-" * 30)
        return user_list
    except Exception as e:
        print(f"获取用户列表失败: {e}")
        return []


if __name__ == '__main__':
    get_all_users()