#!/usr/bin/env python
"""
生成测试数据脚本
"""

import os
import sys
import random
from datetime import timedelta

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 配置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
import django
django.setup()

from django.utils import timezone
from django.contrib.auth.models import User
from secondhand.models import Category, Product, ProductComment, ProductFavorite
from timetable.models import Course, CourseReminder
from foodorder.models import Restaurant, Dish, CartItem, Order, OrderItem, OrderReview

# 随机数据生成函数
def random_date(start_date, end_date):
    """生成指定范围内的随机日期"""
    # 确保日期是时区感知的
    if not hasattr(start_date, 'tzinfo'):
        start_date = timezone.make_aware(start_date)
    if not hasattr(end_date, 'tzinfo'):
        end_date = timezone.make_aware(end_date)
    
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def random_time():
    """生成随机时间字符串"""
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"

def random_price(min_price=1.0, max_price=1000.0):
    """生成随机价格"""
    return round(random.uniform(min_price, max_price), 2)

def random_choice(items):
    """从列表中随机选择一个元素"""
    return random.choice(items)

def random_int(min_val=0, max_val=100):
    """生成随机整数"""
    return random.randint(min_val, max_val)

def random_bool():
    """生成随机布尔值"""
    return random.choice([True, False])

# 生成二手交易数据
def generate_secondhand_data():
    """生成二手交易数据"""
    print("正在生成二手交易数据...")
    
    # 创建商品分类
    categories = [
        "电子产品", "书籍", "服装", "运动器材", "生活用品", "其他"
    ]
    category_objects = []
    for category_name in categories:
        category, created = Category.objects.get_or_create(name=category_name)
        category_objects.append(category)
    
    # 生成商品数据
    products = []
    product_titles = [
        "iPhone 13 Pro", "MacBook Air M2", "无线鼠标", "机械键盘", "Python编程从入门到精通",
        "高等数学教材", "篮球", "足球", "运动鞋", "羽绒服", "卫衣", "耳机", "充电宝",
        "iPad Pro", "Apple Watch", "小米手环", "联想笔记本", "华为手机", "三星平板",
        "吉他", "尤克里里", "哑铃", "跑步机", "自行车", "滑板", "轮滑鞋",
        "考研资料", "四六级真题", "托福雅思", "会计证教材", "程序员面试宝典",
        "连衣裙", "牛仔裤", "T恤", "外套", "帽子", "围巾", "手套"
    ]
    
    users = list(User.objects.all())
    
    for i in range(200):  # 生成200个商品
        product = Product.objects.create(
            name=f"{random_choice(product_titles)} {i+1}",
            description=f"这是一个优质的{random_choice(product_titles)}，成色很好，功能正常。",
            price=random_price(10.0, 2000.0),
            category=random_choice(category_objects),
            user=random_choice(users),
            status=random_choice([0, 0, 0, 1]),  # 75%在售，25%已售出
            contact="13800138000",
            images=[],
            created_at=random_date(timezone.now() - timedelta(days=30), timezone.now())
        )
        products.append(product)
    
    # 生成商品评论
    for product in products:
        for _ in range(random_int(0, 5)):  # 每个商品0-5条评论
            ProductComment.objects.create(
                product=product,
                user=random_choice(users),
                content=f"这是一条关于{product.name}的评论，质量很好！",
                created_at=random_date(product.created_at, timezone.now())
            )
    
    # 生成商品收藏
    for product in products:
        for _ in range(random_int(0, 10)):  # 每个商品0-10个收藏
            ProductFavorite.objects.get_or_create(
                product=product,
                user=random_choice(users),
                defaults={'created_at': random_date(product.created_at, timezone.now())}
            )
    
    print(f"已生成{len(products)}个商品，{ProductComment.objects.count()}条评论，{ProductFavorite.objects.count()}个收藏")

# 生成课程表数据
def generate_timetable_data():
    """生成课程表数据"""
    print("正在生成课程表数据...")
    
    users = list(User.objects.all())
    
    # 课程名称列表
    course_names = [
        "高等数学", "大学英语", "计算机导论", "线性代数", "概率论与数理统计",
        "大学物理", "电路原理", "数据结构", "操作系统", "计算机网络",
        "数据库原理", "软件工程", "人工智能", "机器学习", "深度学习"
    ]
    
    # 教师列表
    teachers = [
        "张老师", "李老师", "王老师", "刘老师", "陈老师",
        "杨老师", "赵老师", "黄老师", "周老师", "吴老师"
    ]
    
    # 教室列表
    classrooms = [
        "教1-101", "教1-102", "教2-203", "教2-204", "教3-305",
        "教3-306", "实验楼-101", "实验楼-102", "图书馆-501", "图书馆-502"
    ]
    
    # 生成课程数据
    courses = []
    for i in range(100):  # 生成100门课程
        course = Course.objects.create(
            user=random_choice(users),
            name=f"{random_choice(course_names)} {i+1}",
            teacher=random_choice(teachers),
            location=random_choice(classrooms),
            day_of_week=random_int(1, 7),  # 周一到周日
            start_time=f"{random_int(8, 12):02d}:{random_int(0, 59):02d}:00",
            end_time=f"{random_int(13, 18):02d}:{random_int(0, 59):02d}:00",
            credit=random_choice([2.0, 3.0, 4.0]),
            created_at=random_date(timezone.now() - timedelta(days=60), timezone.now())
        )
        courses.append(course)
    
    # 生成课程提醒
    for course in courses:
        if random_bool():
            CourseReminder.objects.get_or_create(
                course=course,
                defaults={
                    'reminder_minutes': random_int(5, 30),  # 提前5-30分钟提醒
                    'is_enabled': random_bool()
                }
            )
    
    print(f"已生成{len(courses)}门课程，{CourseReminder.objects.count()}个课程提醒")

# 生成校园点餐数据
def generate_foodorder_data():
    """生成校园点餐数据"""
    print("正在生成校园点餐数据...")
    
    users = list(User.objects.all())
    
    # 餐厅名称列表
    restaurant_names = [
        "学生餐厅", "教工餐厅", "清真餐厅", "西式快餐", "奶茶店",
        "面馆", "盖浇饭", "麻辣烫", "烧烤店", "水果店"
    ]
    
    # 菜品分类
    dish_categories = [
        "主食", "炒菜", "汤品", "小吃", "饮料",
        "甜点", "水果", "套餐", "烧烤", "麻辣烫"
    ]
    
    # 生成餐厅数据
    restaurants = []
    for i in range(20):  # 生成20个餐厅
        restaurant = Restaurant.objects.create(
            name=f"{restaurant_names[i % len(restaurant_names)]} {i+1}",
            description=f"这是{restaurant_names[i % len(restaurant_names)]}，提供各种美味的食物。",
            location=f"校园{i+1}号楼附近",
            opening_hours="06:30-22:00",
            created_at=random_date(timezone.now() - timedelta(days=90), timezone.now())
        )
        restaurants.append(restaurant)
    
    # 生成菜品数据
    dishes = []
    dish_names = [
        "宫保鸡丁", "鱼香肉丝", "红烧肉", "糖醋里脊", "麻婆豆腐",
        "西红柿炒蛋", "青菜", "米饭", "馒头", "面条",
        "汉堡", "炸鸡", "薯条", "可乐", "奶茶",
        "水果沙拉", "冰淇淋", "蛋糕", "烧烤", "麻辣烫"
    ]
    
    for restaurant in restaurants:
        for i in range(20):  # 每个餐厅20个菜品
            dish = Dish.objects.create(
                restaurant=restaurant,
                name=f"{random_choice(dish_names)} {i+1}",
                description=f"这是{restaurant.name}的{random_choice(dish_names)}，味道很好！",
                price=random_price(5.0, 50.0),
                status=random_choice([0, 1]),
                created_at=random_date(restaurant.created_at, timezone.now())
            )
            dishes.append(dish)
    
    # 生成购物车数据
    for user in users:
        for _ in range(random_int(2, 10)):  # 每个用户2-10个购物车商品
            CartItem.objects.get_or_create(
                user=user,
                dish=random_choice(dishes),
                defaults={
                    'quantity': random_int(1, 5),
                    'created_at': random_date(timezone.now() - timedelta(days=7), timezone.now())
                }
            )
    
    # 生成订单数据
    orders = []
    for user in users:
        for _ in range(random_int(5, 20)):  # 每个用户5-20个订单
            restaurant = random_choice(restaurants)
            order = Order.objects.create(
                user=user,
                restaurant=restaurant,
                total_price=random_price(20.0, 200.0),
                status=random_choice([0, 1, 2, 3, 4, 5]),  # 各种状态的订单
                payment_method=random_choice([0, 1, 2]),
                delivery_address=f"学生宿舍{random_int(1, 20)}号楼{random_int(1, 6)}层{random_int(101, 606)}",
                created_at=random_date(timezone.now() - timedelta(days=30), timezone.now())
            )
            orders.append(order)
    
    # 生成订单项数据
    for order in orders:
        for _ in range(random_int(1, 5)):  # 每个订单1-5个商品
            OrderItem.objects.create(
                order=order,
                dish=random_choice(dishes),
                quantity=random_int(1, 3),
                price=random_price(10.0, 50.0)
            )
    
    # 生成订单评价
    for order in orders:
        if order.status == 4:  # 只有已完成的订单可以评价
            OrderReview.objects.create(
                order=order,
                rating=random_int(1, 5),
                content=f"这是对订单{order.id}的评价，服务很好！",
                created_at=random_date(order.created_at, timezone.now())
            )
    
    print(f"已生成{len(restaurants)}个餐厅，{len(dishes)}个菜品，{CartItem.objects.count()}个购物车商品")
    print(f"已生成{len(orders)}个订单，{OrderItem.objects.count()}个订单项，{OrderReview.objects.count()}个订单评价")

# 主函数
def main():
    """主函数"""
    print("开始生成测试数据...")
    
    # 生成二手交易数据
    generate_secondhand_data()
    
    # 生成课程表数据
    generate_timetable_data()
    
    # 生成校园点餐数据
    generate_foodorder_data()
    
    print("测试数据生成完成！")

if __name__ == '__main__':
    main()