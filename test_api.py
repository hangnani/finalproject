import requests

def test_users_api():
    # 获取token
    login_url = 'http://localhost:8000/api/users/login/'
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    print('正在登录...')
    login_response = requests.post(login_url, json=login_data)
    if login_response.status_code != 200:
        print(f'登录失败: {login_response.status_code}')
        print(login_response.text)
        return
    
    token = login_response.json().get('access')
    print(f'登录成功，获取到token: {token[:20]}...')
    
    # 使用token获取用户列表
    users_url = 'http://localhost:8000/api/users/users/'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    print('\n正在获取用户列表...')
    users_response = requests.get(users_url, headers=headers)
    if users_response.status_code != 200:
        print(f'获取用户列表失败: {users_response.status_code}')
        print(users_response.text)
        return
    
    users = users_response.json()
    print(f'获取到 {len(users)} 个用户:')
    for user in users:
        print(f'- {user.get("username")} (ID: {user.get("id")}, 邮箱: {user.get("email")})')
        
        # 检查是否是yang用户
        if user.get('username') == 'yang':
            print(f'  找到yang用户: {user}')

if __name__ == '__main__':
    test_users_api()
