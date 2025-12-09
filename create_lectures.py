import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
os.chdir('./backend')
django.setup()

from django.contrib.auth.models import User
from timetable.models import Lecture
from django.utils import timezone
import datetime

# 获取管理员用户
admin_user = User.objects.get(username='admin')

# 创建5个讲座
for i in range(5):
    title = f'智能校园系列讲座第{i+1}讲'
    speaker = f'专家{i+1}'
    lecture_date = timezone.now().date() + datetime.timedelta(days=i*2)
    start_time = datetime.time(14, 0)
    end_time = datetime.time(16, 0)
    location = f'学术报告厅{i+1}'
    description = f'这是智能校园系列讲座的第{i+1}讲，主题是校园数字化转型。'
    
    # 创建讲座
    lecture = Lecture.objects.create(
        title=title,
        speaker=speaker,
        lecture_date=lecture_date,
        start_time=start_time,
        end_time=end_time,
        location=location,
        description=description,
        created_by=admin_user
    )
    
    print(f'创建了讲座: {title}')

print('\n所有讲座创建完成！')