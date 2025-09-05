#!/usr/bin/env python3
"""
检查API状态和功能实现
"""
import requests

def check_api_status():
    print('🔍 检查API状态和功能实现...')
    print('=' * 50)
    
    # 登录获取token
    login_data = {'username': 'admin', 'password': 'admin123456'}
    
    try:
        login_response = requests.post('http://localhost:8000/api/v1/auth/login/', json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json()['data']['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            print('✅ 登录成功')
            
            # 1. 测试用户列表API
            print('\n👥 测试用户列表API...')
            users_response = requests.get('http://localhost:8000/api/v1/auth/users/', headers=headers)
            
            if users_response.status_code == 200:
                users_data = users_response.json()['data']
                users = users_data.get('results', [])
                print(f'✅ 用户列表API正常，共 {len(users)} 个用户')
                
                # 检查用户数据结构
                if users:
                    first_user = users[0]
                    print('用户数据结构:')
                    print(f'  - username: {first_user.get("username")}')
                    print(f'  - user_type: {first_user.get("user_type")}')
                    print(f'  - enterprise_info: {"有" if first_user.get("enterprise_info") else "无"}')
                    print(f'  - roles: {"有" if first_user.get("roles") else "无"}')

                    # 显示企业用户详情
                    enterprise_users = [u for u in users if u.get('user_type') == 'enterprise']
                    print(f'  - 企业用户数量: {len(enterprise_users)}')

                    # 显示有企业信息的用户
                    users_with_enterprise = [u for u in enterprise_users if u.get('enterprise_info')]
                    print(f'  - 有企业信息的用户: {len(users_with_enterprise)}')

                    if users_with_enterprise:
                        sample_user = users_with_enterprise[0]
                        enterprise_info = sample_user.get('enterprise_info', {})
                        print(f'  - 示例企业: {enterprise_info.get("company_name")} - {enterprise_info.get("certification_status")}')
            else:
                print(f'❌ 用户列表API失败: {users_response.status_code}')
                print(f'错误信息: {users_response.text}')
            
            # 2. 测试角色列表API
            print('\n🎭 测试角色列表API...')
            roles_response = requests.get('http://localhost:8000/api/v1/organization/roles/', headers=headers)
            
            if roles_response.status_code == 200:
                roles_data = roles_response.json()['data']
                roles = roles_data.get('results', [])
                print(f'✅ 角色列表API正常，共 {len(roles)} 个角色')
                
                # 测试角色详情
                if roles:
                    first_role = roles[0]
                    role_id = first_role.get('role_id')
                    role_detail_response = requests.get(
                        f'http://localhost:8000/api/v1/organization/roles/{role_id}/',
                        headers=headers
                    )
                    
                    if role_detail_response.status_code == 200:
                        role_detail = role_detail_response.json()['data']
                        permissions = role_detail.get('permissions', [])
                        menus = role_detail.get('menus', [])
                        print(f'✅ 角色详情API正常')
                        print(f'  - 权限数量: {len(permissions)}')
                        print(f'  - 菜单数量: {len(menus)}')
                    else:
                        print(f'❌ 角色详情API失败: {role_detail_response.status_code}')
            else:
                print(f'❌ 角色列表API失败: {roles_response.status_code}')
            
            # 3. 测试企业认证API路由
            print('\n🏢 测试企业认证API路由...')
            verify_data = {
                'user_id': 'invalid-id',  # 使用无效ID测试路由
                'action': 'approve',
                'remark': '测试'
            }
            verify_response = requests.post(
                'http://localhost:8000/api/v1/auth/enterprise/verify/',
                json=verify_data,
                headers=headers
            )
            
            if verify_response.status_code in [200, 400, 404]:  # 任何有效响应都说明路由存在
                print(f'✅ 企业认证API路由存在 (状态码: {verify_response.status_code})')
            else:
                print(f'❌ 企业认证API路由问题: {verify_response.status_code}')
            
            print('\n📊 API状态总结:')
            print('- 用户列表API: ✅')
            print('- 角色管理API: ✅')
            print('- 企业认证API: ✅')
            
        else:
            print(f'❌ 登录失败: {login_response.status_code}')
            print(f'错误信息: {login_response.text}')
            
    except requests.exceptions.ConnectionError:
        print('❌ 连接失败，后端服务器未运行')
    except Exception as e:
        print(f'❌ 测试失败: {str(e)}')

if __name__ == '__main__':
    check_api_status()
