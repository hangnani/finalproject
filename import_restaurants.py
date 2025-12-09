#!/usr/bin/env python3
"""
导入餐厅数据的脚本
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

from foodorder.models import Restaurant


def import_restaurants():
    """导入餐厅数据"""
    try:
        # 从普通用户页面复制的餐厅数据
        restaurants_data = [
            {
                'name': '学生餐厅',
                'description': '提供各种中式快餐，价格实惠，口味正宗',
                'location': '学生食堂一楼',
                'opening_hours': '06:30-22:00'
            },
            {
                'name': '教工餐厅',
                'description': '环境优雅，菜品精致，适合师生聚餐',
                'location': '行政楼二楼',
                'opening_hours': '07:00-21:30'
            },
            {
                'name': '清真餐厅',
                'description': '严格按照清真饮食规定制作，口味独特',
                'location': '学生食堂二楼',
                'opening_hours': '06:30-22:00'
            },
            {
                'name': '西式快餐',
                'description': '汉堡、薯条、炸鸡等西式快餐',
                'location': '学生活动中心',
                'opening_hours': '10:00-22:30'
            },
            {
                'name': '素食餐厅',
                'description': '健康素食，营养均衡，适合素食爱好者',
                'location': '学生食堂三楼',
                'opening_hours': '07:30-21:00'
            },
            {
                'name': '奶茶店',
                'description': '各类奶茶、果茶、甜品，休闲好去处',
                'location': '商业街',
                'opening_hours': '09:00-23:00'
            },
            {
                'name': '特色小吃街',
                'description': '各种地方特色小吃，品种丰富',
                'location': '商业街',
                'opening_hours': '11:00-22:00'
            }
        ]
        
        print("导入餐厅数据：")
        print("-" * 30)
        
        for restaurant_data in restaurants_data:
            try:
                # 检查餐厅是否已存在
                existing_restaurant = Restaurant.objects.filter(name=restaurant_data['name']).first()
                if existing_restaurant:
                    print(f"✓ {restaurant_data['name']}: 已存在，跳过")
                    continue
                
                # 创建餐厅
                restaurant = Restaurant.objects.create(**restaurant_data)
                print(f"✓ {restaurant.name}: 导入成功")
            except Exception as e:
                print(f"✗ {restaurant_data['name']}: 导入失败 - {e}")
        
        print("-" * 30)
        print(f"导入完成！总餐厅数量：{Restaurant.objects.count()}")
        return True
    except Exception as e:
        print(f"导入餐厅数据失败: {e}")
        return False


if __name__ == '__main__':
    import_restaurants()