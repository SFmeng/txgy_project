#!/usr/bin/env python
"""
组织架构系统功能测试脚本
"""
import requests
import json
import time

BASE_URL = 'http://localhost:8000'

def test_login():
    """测试登录功能"""
    print("\n🔍 测试用户登录...")
    
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
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 登录成功")
            return result['data']['access_token']
        else:
            print(f"❌ 登录失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 登录请求失败: {str(e)}")
        return None

def test_user_permissions(token):
    """测试获取用户权限和菜单"""
    print("\n🔍 测试获取用户权限和菜单...")
    
    try:
        response = requests.get(
            f'{BASE_URL}/api/v1/organization/user/permissions/',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            permissions = result['data']['permissions']
            menus = result['data']['menus']
            
            print(f"✅ 获取权限成功，共 {len(permissions)} 个权限")
            print(f"✅ 获取菜单成功，共 {len(menus)} 个菜单")
            
            # 显示部分权限信息
            if permissions:
                print(f"   权限示例: {permissions[0]['perm_name']}")
            
            # 显示部分菜单信息
            if menus:
                print(f"   菜单示例: {menus[0]['menu_name']}")
            
            return True
        else:
            print(f"❌ 获取权限失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 权限请求失败: {str(e)}")
        return False

def test_roles_api(token):
    """测试角色管理API"""
    print("\n🔍 测试角色管理API...")
    
    try:
        response = requests.get(
            f'{BASE_URL}/api/v1/organization/roles/',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            roles = result['data']['results']
            print(f"✅ 获取角色列表成功，共 {len(roles)} 个角色")
            
            # 显示角色信息
            for role in roles:
                print(f"   - {role['role_name']}: {role['description']}")
            
            return True
        else:
            print(f"❌ 获取角色失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 角色请求失败: {str(e)}")
        return False

def test_permissions_api(token):
    """测试权限管理API"""
    print("\n🔍 测试权限管理API...")
    
    try:
        response = requests.get(
            f'{BASE_URL}/api/v1/organization/permissions/',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            permissions = result['data']
            print(f"✅ 获取权限列表成功，共 {len(permissions)} 个权限")
            
            # 按模块分组显示
            modules = {}
            for perm in permissions:
                module = perm['module']
                if module not in modules:
                    modules[module] = []
                modules[module].append(perm['perm_name'])
            
            for module, perms in modules.items():
                print(f"   {module}: {len(perms)} 个权限")
            
            return True
        else:
            print(f"❌ 获取权限失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 权限请求失败: {str(e)}")
        return False

def test_menus_api(token):
    """测试菜单管理API"""
    print("\n🔍 测试菜单管理API...")
    
    try:
        response = requests.get(
            f'{BASE_URL}/api/v1/organization/menus/tree/',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            menus = result['data']
            print(f"✅ 获取菜单树成功，共 {len(menus)} 个顶级菜单")
            
            # 显示菜单结构
            def show_menu_tree(menus, level=0):
                for menu in menus:
                    indent = "  " * level
                    print(f"   {indent}- {menu['menu_name']} ({menu['path']})")
                    if 'children' in menu and menu['children']:
                        show_menu_tree(menu['children'], level + 1)
            
            show_menu_tree(menus)
            return True
        else:
            print(f"❌ 获取菜单失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 菜单请求失败: {str(e)}")
        return False

def test_system_configs_api(token):
    """测试系统配置API"""
    print("\n🔍 测试系统配置API...")
    
    try:
        response = requests.get(
            f'{BASE_URL}/api/v1/organization/configs/',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            configs = result['data']
            print(f"✅ 获取系统配置成功，共 {len(configs)} 个配置项")
            return True
        else:
            print(f"❌ 获取系统配置失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 系统配置请求失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 防腐保温智慧平台 - 组织架构系统功能测试")
    print("=" * 60)
    
    # 等待服务器启动
    time.sleep(2)
    
    # 1. 测试登录
    token = test_login()
    if not token:
        print("\n❌ 登录失败，无法继续测试")
        return
    
    # 2. 测试用户权限和菜单
    permissions_success = test_user_permissions(token)
    
    # 3. 测试角色管理API
    roles_success = test_roles_api(token)
    
    # 4. 测试权限管理API
    permissions_api_success = test_permissions_api(token)
    
    # 5. 测试菜单管理API
    menus_success = test_menus_api(token)
    
    # 6. 测试系统配置API
    configs_success = test_system_configs_api(token)
    
    # 总结
    print("\n" + "=" * 60)
    print("📋 测试结果总结:")
    print(f"- 用户登录: {'✅ 成功' if token else '❌ 失败'}")
    print(f"- 用户权限菜单: {'✅ 成功' if permissions_success else '❌ 失败'}")
    print(f"- 角色管理API: {'✅ 成功' if roles_success else '❌ 失败'}")
    print(f"- 权限管理API: {'✅ 成功' if permissions_api_success else '❌ 失败'}")
    print(f"- 菜单管理API: {'✅ 成功' if menus_success else '❌ 失败'}")
    print(f"- 系统配置API: {'✅ 成功' if configs_success else '❌ 失败'}")
    
    all_success = all([
        token, permissions_success, roles_success, 
        permissions_api_success, menus_success, configs_success
    ])
    
    if all_success:
        print("\n🎉 所有组织架构功能测试通过！")
        print("\n📋 系统功能:")
        print("- ✅ 用户认证和权限管理")
        print("- ✅ 角色管理系统")
        print("- ✅ 权限管理系统")
        print("- ✅ 动态菜单系统")
        print("- ✅ 系统配置管理")
        print("\n🌐 访问地址:")
        print("- 前端应用: http://localhost:3001")
        print("- 后台管理: http://localhost:3001/admin")
        print("- 后端API: http://localhost:8000")
        print("\n🔑 登录信息:")
        print("- 用户名: admin")
        print("- 密码: admin123456")
        print("\n✨ 组织架构系统已完全就绪，可以开始使用！")
    else:
        print("\n❌ 部分功能测试失败，请检查系统配置")

if __name__ == '__main__':
    main()
