#!/usr/bin/env python3
"""
强制删除test_0菜单（先从角色中移除，再删除菜单）
"""
import requests

def force_delete_test_menu():
    print('🔍 强制删除test_0菜单...')
    print('=' * 50)
    
    # 登录获取token
    login_data = {'username': 'admin', 'password': 'admin123456'}
    
    try:
        login_response = requests.post('http://localhost:8000/api/v1/auth/login/', json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json()['data']['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            print('✅ 登录成功')
            
            # 1. 查找test_0菜单
            print('\n🔍 查找test_0菜单...')
            menu_response = requests.get(
                'http://localhost:8000/api/v1/organization/menus/?terminal=pc', 
                headers=headers
            )
            
            if menu_response.status_code == 200:
                menus = menu_response.json()['data']
                
                def find_menu_by_name(menu_list, target_name):
                    for menu in menu_list:
                        if menu.get('menu_name') == target_name:
                            return menu
                        if menu.get('children'):
                            found = find_menu_by_name(menu['children'], target_name)
                            if found:
                                return found
                    return None
                
                test_menu = find_menu_by_name(menus, 'test_0')
                
                if test_menu:
                    menu_id = test_menu.get('menu_id', '')
                    print(f'✅ 找到test_0菜单 (ID: {menu_id})')
                    
                    # 2. 获取所有角色
                    print('\n🎭 获取所有角色...')
                    roles_response = requests.get('http://localhost:8000/api/v1/organization/roles/', headers=headers)
                    
                    if roles_response.status_code == 200:
                        roles = roles_response.json()['data']['results']
                        print(f'✅ 找到 {len(roles)} 个角色')
                        
                        # 3. 从每个角色中移除test_0菜单
                        for role in roles:
                            try:
                                role_id = role.get('role_id', '')
                                role_name = role.get('role_name', '')
                                print(f'\\n🔄 处理角色: {role_name}')
                                
                                # 获取角色详情
                                role_detail_response = requests.get(
                                    f'http://localhost:8000/api/v1/organization/roles/{role_id}/',
                                    headers=headers
                                )
                                
                                if role_detail_response.status_code == 200:
                                    role_data = role_detail_response.json()['data']
                                    current_menu_ids = [menu['menu_id'] for menu in role_data.get('menus', [])]
                                    
                                    if menu_id in current_menu_ids:
                                        print(f'   📋 角色 {role_name} 包含test_0菜单，正在移除...')
                                        
                                        # 移除test_0菜单ID
                                        current_menu_ids.remove(menu_id)
                                        
                                        # 重新分配菜单
                                        assign_response = requests.post(
                                            'http://localhost:8000/api/v1/organization/assign/menus/',
                                            json={
                                                'role_id': role_id,
                                                'menu_ids': current_menu_ids
                                            },
                                            headers=headers
                                        )
                                        
                                        if assign_response.status_code == 200:
                                            print(f'   ✅ 从角色 {role_name} 中移除test_0菜单成功')
                                        else:
                                            print(f'   ❌ 从角色 {role_name} 中移除菜单失败: {assign_response.status_code}')
                                    else:
                                        print(f'   ℹ️ 角色 {role_name} 不包含test_0菜单')
                                else:
                                    print(f'   ❌ 获取角色 {role_name} 详情失败')
                            except Exception as e:
                                print(f'   ❌ 处理角色 {role_name} 时出错: {str(e)}')
                        
                        # 4. 现在删除菜单
                        print(f'\\n🗑️ 删除test_0菜单...')
                        delete_response = requests.delete(
                            f'http://localhost:8000/api/v1/organization/menus/{menu_id}/',
                            headers=headers
                        )
                        
                        if delete_response.status_code == 200:
                            print('✅ test_0菜单删除成功')
                        else:
                            print(f'❌ 删除失败: {delete_response.status_code}')
                            print(f'错误信息: {delete_response.text}')
                    else:
                        print('❌ 获取角色列表失败')
                else:
                    print('ℹ️ 没有找到test_0菜单，可能已经被删除')
            else:
                print(f'❌ 获取菜单失败: {menu_response.status_code}')
        else:
            print('❌ 登录失败')
            
    except requests.exceptions.ConnectionError:
        print('❌ 连接失败，请确保后端服务器正在运行')
    except Exception as e:
        print(f'❌ 操作过程中出现错误: {str(e)}')

if __name__ == '__main__':
    force_delete_test_menu()
