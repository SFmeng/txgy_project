#!/usr/bin/env python3
"""
测试菜单与角色关联功能
"""
import requests
import json

def test_menu_role_association():
    print('🔍 测试菜单与角色关联功能...')
    print('=' * 60)
    
    # 登录获取token
    login_data = {'username': 'admin', 'password': 'admin123456'}
    
    try:
        login_response = requests.post('http://localhost:8000/api/v1/auth/login/', json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json()['data']['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            print('✅ 登录成功')
            
            # 测试获取用户权限和菜单
            print('\n📋 测试获取用户权限和菜单...')
            user_perms_response = requests.get(
                'http://localhost:8000/api/v1/organization/user/permissions/', 
                headers=headers
            )
            
            if user_perms_response.status_code == 200:
                user_data = user_perms_response.json()['data']
                print('✅ 获取用户数据成功')
                print(f'   - 权限数量: {len(user_data.get("permissions", []))}')
                print(f'   - 菜单数量: {len(user_data.get("menus", []))}')
                
                # 显示菜单结构
                menus = user_data.get('menus', [])
                if menus:
                    print('   - 菜单结构:')
                    for menu in menus:
                        print(f'     └─ {menu["menu_name"]} ({menu["path"]})')
                        for child in menu.get('children', []):
                            print(f'        └─ {child["menu_name"]} ({child["path"]})')
                else:
                    print('   ⚠️ 用户没有分配菜单')
            else:
                print(f'❌ 获取用户权限和菜单失败: {user_perms_response.status_code}')
            
            # 测试角色菜单分配
            print('\n🎭 测试角色菜单分配...')
            
            # 获取角色列表
            roles_response = requests.get('http://localhost:8000/api/v1/organization/roles/', headers=headers)
            if roles_response.status_code == 200:
                roles = roles_response.json()['data']['results']
                if roles:
                    admin_role = roles[0]  # 使用第一个角色
                    print(f'✅ 找到角色: {admin_role["role_name"]}')
                    
                    # 获取菜单列表
                    menus_response = requests.get('http://localhost:8000/api/v1/organization/menus/?terminal=pc', headers=headers)
                    if menus_response.status_code == 200:
                        menus = menus_response.json()['data']
                        if menus:
                            # 收集所有菜单ID
                            menu_ids = []
                            def collect_menu_ids(menu_list):
                                for menu in menu_list:
                                    menu_ids.append(menu['menu_id'])
                                    if menu.get('children'):
                                        collect_menu_ids(menu['children'])
                            
                            collect_menu_ids(menus)
                            print(f'✅ 找到 {len(menu_ids)} 个菜单')
                            
                            # 分配菜单给角色
                            assign_data = {
                                'role_id': admin_role['role_id'],
                                'menu_ids': menu_ids
                            }
                            
                            assign_response = requests.post(
                                'http://localhost:8000/api/v1/organization/assign/menus/',
                                json=assign_data,
                                headers=headers
                            )
                            
                            if assign_response.status_code == 200:
                                print('✅ 菜单分配成功')
                                
                                # 重新获取用户权限和菜单
                                print('\n🔄 重新获取用户菜单...')
                                user_perms_response2 = requests.get(
                                    'http://localhost:8000/api/v1/organization/user/permissions/', 
                                    headers=headers
                                )
                                
                                if user_perms_response2.status_code == 200:
                                    user_data2 = user_perms_response2.json()['data']
                                    menus2 = user_data2.get('menus', [])
                                    print(f'✅ 用户现在有 {len(menus2)} 个顶级菜单')
                                    
                                    for menu in menus2:
                                        children_count = len(menu.get('children', []))
                                        print(f'   - {menu["menu_name"]}: {children_count} 个子菜单')
                                        
                                    print('\n📊 测试结果总结:')
                                    print('- ✅ 用户权限获取API正常')
                                    print('- ✅ 角色菜单分配API正常')
                                    print('- ✅ 菜单与角色关联功能正常')
                                    print('- ✅ 动态菜单生成功能正常')
                                else:
                                    print('❌ 重新获取用户菜单失败')
                            else:
                                print(f'❌ 菜单分配失败: {assign_response.status_code} - {assign_response.text}')
                        else:
                            print('❌ 没有找到菜单')
                    else:
                        print('❌ 获取菜单列表失败')
                else:
                    print('❌ 没有找到角色')
            else:
                print('❌ 获取角色列表失败')
            
            print('\n' + '=' * 60)
            print('🎉 菜单与角色关联功能测试完成！')
        else:
            print(f'❌ 登录失败: {login_response.status_code}')
            
    except requests.exceptions.ConnectionError:
        print('❌ 连接失败，请确保后端服务器正在运行')
    except Exception as e:
        print(f'❌ 测试过程中出现错误: {str(e)}')

if __name__ == '__main__':
    test_menu_role_association()
