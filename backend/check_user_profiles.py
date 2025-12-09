#!/usr/bin/env python3
"""
检查用户和用户档案的关系
"""

import os
import sys

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
import django
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile

# 检查创建的二手交易用户
usernames = ['ershou1', 'ershou2', 'ershou3']

for username in usernames:
    try:
        user = User.objects.get(username=username)
        has_profile = UserProfile.objects.filter(user=user).exists()
        print(f'User: {username}, Has Profile: {has_profile}')
        
        # 如果没有UserProfile，创建一个
        if not has_profile:
            UserProfile.objects.create(
                user=user,
                student_id=f'student_{username}',
                phone='13800138000'
            )
            print(f'✓ Created UserProfile for {username}')
    except User.DoesNotExist:
        print(f'✗ User {username} not found')

print('\nAll checks completed!')
