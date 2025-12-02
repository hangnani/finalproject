#!/usr/bin/env python
"""
为所有餐厅生成菜品数据脚本
"""

import os
import sys
import random
from datetime import timedelta

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
import django
django.setup()

from django.utils import timezone
from foodorder.models import Restaurant, Dish

def generate_dishes_for_all_restaurants():
    """为所有餐厅生成菜品数据"""
    print("正在为所有餐厅生成菜品数据...")
    
    # 菜品名称列表
    dish_names = [
        "宫保鸡丁", "鱼香肉丝", "红烧肉", "糖醋里脊", "麻婆豆腐",
        "西红柿炒蛋", "青菜", "米饭", "馒头", "面条",
        "汉堡", "炸鸡", "薯条", "可乐", "奶茶",
        "水果沙拉", "冰淇淋", "蛋糕", "烧烤", "麻辣烫"
    ]
    
    # 获取所有餐厅
    restaurants = Restaurant.objects.all()
    
    # 为每个餐厅生成菜品
    for restaurant in restaurants:
        print(f"正在为餐厅 {restaurant.name} (ID: {restaurant.id}) 生成菜品...")
        
        # 检查是否已有菜品
        existing_dishes = Dish.objects.filter(restaurant=restaurant).count()
        if existing_dishes >= 20:
            print(f"  餐厅 {restaurant.name} 已有 {existing_dishes} 个菜品，跳过")
            continue
        
        # 生成20个菜品
        for i in range(20):
            Dish.objects.create(
                restaurant=restaurant,
                name=f"{random.choice(dish_names)} {i+1}",
                description=f"这是{restaurant.name}的{random.choice(dish_names)}，味道很好！",
                price=round(random.uniform(5.0, 50.0), 2),
                status=random.choice([0, 1]),
                created_at=timezone.now()
            )
        
        print(f"  已为餐厅 {restaurant.name} 生成20个菜品")
    
    print(f"\n已为所有餐厅生成菜品数据！")
    print(f"总餐厅数: {Restaurant.objects.count()}")
    print(f"总菜品数: {Dish.objects.count()}")


if __name__ == '__main__':
    generate_dishes_for_all_restaurants()
