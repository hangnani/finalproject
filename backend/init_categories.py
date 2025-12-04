import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from secondhand.models import Category

# 定义要创建的分类
categories = [
    {'name': '书籍'},
    {'name': '电子产品'},
    {'name': '生活用品'},
    {'name': '运动器材'},
    {'name': '其他'}
]

# 创建分类
def init_categories():
    print('开始初始化分类数据...')
    
    created_count = 0
    for cat_data in categories:
        category, created = Category.objects.get_or_create(**cat_data)
        if created:
            print(f'创建分类: {category.name}')
            created_count += 1
        else:
            print(f'分类已存在: {category.name}')
    
    print(f'\n初始化完成！创建了 {created_count} 个分类，总共 {Category.objects.count()} 个分类。')
    print('现有分类:', list(Category.objects.values_list('id', 'name')))

if __name__ == '__main__':
    init_categories()
