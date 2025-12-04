import requests
import json

# 测试商品发布API
def test_product_create():
    # 先登录获取token
    login_url = 'http://127.0.0.1:8000/api/users/login/'
    login_data = {
        'username': 'test',
        'password': 'test123456'
    }
    
    print('尝试登录...')
    login_response = requests.post(login_url, json=login_data)
    print(f'登录状态码: {login_response.status_code}')
    
    if login_response.status_code != 200:
        print(f'登录失败: {login_response.text}')
        # 尝试注册新用户
        register_url = 'http://127.0.0.1:8000/api/users/register/'
        register_data = {
            'username': 'test',
            'password': 'test123456',
            'password_confirm': 'test123456',
            'email': 'test@example.com',
            'name': '测试用户',
            'student_id': '20210001',
            'phone': '13800138000'
        }
        print('尝试注册新用户...')
        register_response = requests.post(register_url, json=register_data)
        print(f'注册状态码: {register_response.status_code}')
        print(f'注册结果: {register_response.text}')
        
        # 重新登录
        login_response = requests.post(login_url, json=login_data)
        print(f'重新登录状态码: {login_response.status_code}')
        if login_response.status_code != 200:
            print(f'登录失败: {login_response.text}')
            return
    
    login_result = login_response.json()
    token = login_result.get('access')
    print(f'获取到token: {token}')
    
    # 测试商品发布
    product_url = 'http://127.0.0.1:8000/api/secondhand/products/'
    product_data = {
        'name': '测试商品',
        'description': '测试描述',
        'price': 100.00,
        'category': 1,
        'status': 0,
        'images': [],
        'contact': '123456789'
    }
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print('\n尝试发布商品...')
    product_response = requests.post(product_url, json=product_data, headers=headers)
    print(f'商品发布状态码: {product_response.status_code}')
    print(f'商品发布结果: {product_response.text}')
    print(f'响应头: {product_response.headers}')

if __name__ == '__main__':
    test_product_create()
