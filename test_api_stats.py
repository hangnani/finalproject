#!/usr/bin/env python3
"""
测试API统计数据的脚本
"""

import requests
import json

# API基础URL
BASE_URL = 'http://localhost:8000/api'

def test_api_endpoint(endpoint, token=None):
    """测试API端点是否返回分页数据"""
    url = f'{BASE_URL}{endpoint}'
    headers = {}
    
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        print(f"\nTesting {endpoint}:")
        print(f"Status code: {response.status_code}")
        print(f"Response keys: {list(data.keys())}")
        
        if 'count' in data:
            print(f"Count: {data['count']}")
            print(f"Results length: {len(data.get('results', []))}")
        
        return True, data
    except requests.exceptions.RequestException as e:
        print(f"\nError testing {endpoint}: {e}")
        return False, None

def login():
    """登录获取JWT令牌"""
    url = f'{BASE_URL}/users/login/'
    credentials = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        response = requests.post(url, json=credentials)
        response.raise_for_status()
        data = response.json()
        print(f"\nLogin successful!")
        print(f"Access token: {data['access'][:20]}...")
        return data['access']
    except requests.exceptions.RequestException as e:
        print(f"\nLogin error: {e}")
        print(f"Response: {e.response.text if hasattr(e.response, 'text') else 'No response'}")
        return None

def main():
    """主函数"""
    print("Testing API endpoints for stats...")
    
    # 登录获取令牌
    token = login()
    
    if token:
        # 测试用户列表
        test_api_endpoint('/users/users/', token)
        
        # 测试讲座列表
        test_api_endpoint('/timetable/lectures/', token)
        
        # 测试考试列表
        test_api_endpoint('/timetable/exams/', token)

if __name__ == '__main__':
    main()