#!/usr/bin/env python3
"""
创建二手交易用户并分配商品的脚本
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
from secondhand.models import Product


def create_users_and_assign_products():
    """创建用户并分配商品"""
    try:
        # 要创建的用户名列表
        usernames = ['ershou1', 'ershou2', 'ershou3']
        password = '123456'
        
        # 创建用户
        users = []
        for username in usernames:
            # 检查用户是否已存在
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                print(f"✓ 创建用户: {username}")
            else:
                print(f"✓ 用户已存在: {username}")
            users.append(user)
        
        # 获取所有商品
        products = Product.objects.all()
        total_products = products.count()
        
        print(f"\n总商品数量: {total_products}")
        
        if total_products == 0:
            print("✗ 没有找到商品，跳过分配")
            return False
        
        # 分配商品给用户
        for i, product in enumerate(products):
            # 循环分配给3个用户
            user_index = i % len(users)
            product.user = users[user_index]
            product.save()
            print(f"✓ 商品 {product.name} 已分配给用户: {users[user_index].username}")
        
        print(f"\n✓ 所有商品已分配完成！")
        print(f"✓ 商品总数: {total_products}")
        print(f"✓ 分配给 {len(users)} 个用户")
        
        # 打印最终分配结果
        print(f"\n最终分配结果:")
        for user in users:
            user_products_count = Product.objects.filter(user=user).count()
            print(f"  {user.username}: {user_products_count} 个商品")
        
        return True
    except Exception as e:
        print(f"✗ 执行失败: {e}")
        return False


if __name__ == '__main__':
    create_users_and_assign_products()