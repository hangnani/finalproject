#!/usr/bin/env python3
"""
生成考试数据的脚本
"""

import os
import sys
from datetime import datetime, timedelta

# 添加backend目录到Python路径
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')

# 初始化Django
import django
django.setup()

from timetable.models import Exam, Course
from django.contrib.auth.models import User


def create_exams():
    """创建测试考试数据"""
    try:
        # 获取用户"yang"
        user = User.objects.get(username='yang')
        
        # 先创建3个课程
        courses = []
        for i in range(3):
            course = Course.objects.create(
                user=user,
                name='课程{}'.format(i+1),
                teacher='教师{}'.format(i+1),
                day_of_week=i+1,
                start_time='08:00:00',
                end_time='09:40:00',
                location='教室{}'.format(i+101),
                credit=3.0
            )
            courses.append(course)
            print(f"Created course: {course.name}")
        
        # 然后创建3个考试，关联到课程
        for i in range(3):
            exam = Exam.objects.create(
                user=user,
                name='考试{}'.format(i+1),
                course=courses[i],
                exam_date=datetime.now().date() + timedelta(days=i+1),
                start_time='09:00:00',
                end_time='11:00:00',
                location='教室{}'.format(i+101)
            )
            print(f"Created exam: {exam.name} for course: {exam.course.name}")
        
        print(f"\nTotal courses created: {Course.objects.count()}")
        print(f"Total exams created: {Exam.objects.count()}")
        return True
    except Exception as e:
        print(f"Error creating exams: {e}")
        return False


if __name__ == '__main__':
    create_exams()