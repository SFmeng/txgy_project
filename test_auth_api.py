#!/usr/bin/env python
"""
测试认证API功能
"""
import requests
import json
import time

BASE_URL = 'http://localhost:8000'

def test_backend_connection():
    """测试后端连接"""
    try:
        response = requests.get(f'{BASE_URL}/admin/', timeout=5)
        print(f"✅ 后端连接成功: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ 后端连接失败: {str(e)}")
        return False

def test_register_api():
    """测试注册API"""
    print("\n🔍 测试用户注册API...")
    
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "phone": "13800138000",
        "password": "test123456",
        "password_confirm": "test123456",
        "user_type": "enterprise",
        "real_name": "测试用户",
        "enterprise_info": {
            "company_name": "测试公司",
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
        
        print(f"注册API响应状态: {response.status_code}")
        print(f"注册API响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 注册API测试成功")
            return True
        else:
            print("❌ 注册API测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 注册API请求失败: {str(e)}")
        return False

def test_login_api():
    """测试登录API"""
    print("\n🔍 测试用户登录API...")
    
    login_data = {
        "username": "admin",
        "password": "admin123456",
        "login_type": "password"
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/v1/auth/login/',
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"登录API响应状态: {response.status_code}")
        print(f"登录API响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 登录API测试成功")
            return True
        else:
            print("❌ 登录API测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 登录API请求失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 开始测试认证API功能")
    print("=" * 50)
    
    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(3)
    
    # 测试后端连接
    if not test_backend_connection():
        print("❌ 后端服务器未启动，请先启动后端服务器")
        return
    
    # 测试注册API
    register_success = test_register_api()
    
    # 测试登录API
    login_success = test_login_api()
    
    # 总结
    print("\n" + "=" * 50)
    print("📋 测试结果总结:")
    print(f"- 注册API: {'✅ 成功' if register_success else '❌ 失败'}")
    print(f"- 登录API: {'✅ 成功' if login_success else '❌ 失败'}")
    
    if register_success and login_success:
        print("\n🎉 所有认证API测试通过！")
    else:
        print("\n❌ 部分API测试失败，请检查后端配置")

if __name__ == '__main__':
    main()
