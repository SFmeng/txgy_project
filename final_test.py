#!/usr/bin/env python
"""
最终功能验证脚本
"""
import requests
import json
import time
import random

BASE_URL = 'http://localhost:8000'

def test_new_user_registration():
    """测试新用户注册"""
    print("\n🔍 测试新用户注册...")
    
    # 生成随机用户名和手机号
    random_num = random.randint(1000, 9999)
    register_data = {
        "username": f"newuser{random_num}",
        "email": f"newuser{random_num}@example.com",
        "phone": f"138001380{random_num % 100:02d}",
        "password": "test123456",
        "password_confirm": "test123456",
        "user_type": "enterprise",
        "real_name": f"新用户{random_num}",
        "enterprise_info": {
            "company_name": f"测试公司{random_num}",
            "company_type": "supplier"
        }
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/v1/auth/register/',
            json=register_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"注册响应状态: {response.status_code}")
        if response.status_code == 200:
            print("✅ 新用户注册成功")
            return register_data
        else:
            print(f"❌ 注册失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 注册请求失败: {str(e)}")
        return None

def test_user_login(username, password):
    """测试用户登录"""
    print(f"\n🔍 测试用户登录: {username}")
    
    login_data = {
        "username": username,
        "password": password,
        "login_type": "password"
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/v1/auth/login/',
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"登录响应状态: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ 登录成功")
            print(f"用户信息: {result['data']['user_info']['real_name']}")
            return result['data']['access_token']
        else:
            print(f"❌ 登录失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 登录请求失败: {str(e)}")
        return None

def test_authenticated_request(token):
    """测试认证请求"""
    print(f"\n🔍 测试认证请求...")
    
    try:
        response = requests.get(
            f'{BASE_URL}/api/v1/auth/profile/',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        
        print(f"认证请求响应状态: {response.status_code}")
        if response.status_code == 200:
            print("✅ 认证请求成功")
            return True
        else:
            print(f"❌ 认证请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 认证请求失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 防腐保温智慧平台 - 最终功能验证")
    print("=" * 60)
    
    # 等待服务器启动
    time.sleep(2)
    
    # 1. 测试管理员登录
    admin_token = test_user_login('admin', 'admin123456')
    admin_auth_success = False
    if admin_token:
        admin_auth_success = test_authenticated_request(admin_token)
    
    # 2. 测试新用户注册
    new_user_data = test_new_user_registration()
    new_user_login_success = False
    new_user_auth_success = False
    
    if new_user_data:
        # 3. 测试新用户登录
        new_user_token = test_user_login(new_user_data['username'], new_user_data['password'])
        if new_user_token:
            new_user_login_success = True
            new_user_auth_success = test_authenticated_request(new_user_token)
    
    # 总结
    print("\n" + "=" * 60)
    print("📋 最终测试结果:")
    print(f"- 管理员登录: {'✅ 成功' if admin_token else '❌ 失败'}")
    print(f"- 管理员认证: {'✅ 成功' if admin_auth_success else '❌ 失败'}")
    print(f"- 新用户注册: {'✅ 成功' if new_user_data else '❌ 失败'}")
    print(f"- 新用户登录: {'✅ 成功' if new_user_login_success else '❌ 失败'}")
    print(f"- 新用户认证: {'✅ 成功' if new_user_auth_success else '❌ 失败'}")
    
    all_success = all([admin_token, admin_auth_success, new_user_data, new_user_login_success, new_user_auth_success])
    
    if all_success:
        print("\n🎉 所有功能测试通过！")
        print("\n📋 可用服务:")
        print("- 前端应用: http://localhost:3000")
        print("- 后端API: http://localhost:8000")
        print("- 管理后台: http://localhost:8000/admin/")
        print("\n✨ 登录注册功能已完全修复，可以正常使用！")
    else:
        print("\n❌ 部分功能仍有问题")

if __name__ == '__main__':
    main()
