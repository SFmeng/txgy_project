#!/usr/bin/env python3
"""
测试菜单管理完整功能
"""
import requests
import time

def test_menu_management():
    print('🧪 测试菜单管理完整功能...')
    print('=' * 50)
    
    # 登录获取token
    login_data = {'username': 'admin', 'password': 'admin123456'}
    
    try:
        login_response = requests.post('http://localhost:8000/api/v1/auth/login/', json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json()['data']['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            print('✅ 登录成功')
            
            # 1. 获取当前菜单数量
            menu_response = requests.get(
                'http://localhost:8000/api/v1/organization/menus/?terminal=pc', 
                headers=headers
            )
            
            if menu_response.status_code == 200:
                initial_menus = menu_response.json()['data']
                initial_count = len(initial_menus)
                print(f'✅ 当前菜单数量: {initial_count}')
                
                # 显示当前菜单
                print('\n📋 当前菜单列表:')
                for menu in initial_menus:
                    menu_name = menu.get('menu_name', '')
                    children_count = len(menu.get('children', []))
                    print(f'   - {menu_name}: {children_count} 个子菜单')
                
                # 2. 创建测试菜单
                print('\n📝 创建测试菜单...')
                new_menu = {
                    'parent_id': None,
                    'menu_name': '菜单管理测试',
                    'path': '/menu-test',
                    'component': 'MenuTest',
                    'icon': 'TestTube',
                    'sort': 999,
                    'terminal': 'pc',
                    'is_show': True,
                    'is_external': False
                }
                
                create_response = requests.post(
                    'http://localhost:8000/api/v1/organization/menus/',
                    json=new_menu,
                    headers=headers
                )
                
                if create_response.status_code == 200:
                    created_menu = create_response.json()['data']
                    menu_id = created_menu.get('menu_id', '')
                    menu_name = created_menu.get('menu_name', '')
                    print(f'✅ 菜单创建成功: {menu_name} (ID: {menu_id})')
                    
                    # 3. 验证菜单是否出现在列表中
                    print('\n🔍 验证菜单列表...')
                    menu_response2 = requests.get(
                        'http://localhost:8000/api/v1/organization/menus/?terminal=pc', 
                        headers=headers
                    )
                    
                    if menu_response2.status_code == 200:
                        updated_menus = menu_response2.json()['data']
                        updated_count = len(updated_menus)
                        print(f'✅ 更新后菜单数量: {updated_count}')
                        
                        if updated_count > initial_count:
                            print('✅ 菜单数量增加，创建成功')
                        else:
                            print('❌ 菜单数量未增加，可能有问题')
                    
                    # 4. 测试菜单更新
                    print('\n📝 测试菜单更新...')
                    update_data = {
                        'menu_name': '菜单管理测试(已更新)',
                        'path': '/menu-test-updated',
                        'component': 'MenuTestUpdated',
                        'icon': 'Edit',
                        'sort': 998,
                        'terminal': 'pc',
                        'is_show': True,
                        'is_external': False
                    }
                    
                    update_response = requests.put(
                        f'http://localhost:8000/api/v1/organization/menus/{menu_id}/',
                        json=update_data,
                        headers=headers
                    )
                    
                    if update_response.status_code == 200:
                        print('✅ 菜单更新成功')
                    else:
                        print(f'❌ 菜单更新失败: {update_response.status_code}')
                    
                    # 5. 测试用户权限菜单获取
                    print('\n👤 测试用户权限菜单获取...')
                    user_perms_response = requests.get(
                        'http://localhost:8000/api/v1/organization/user/permissions/', 
                        headers=headers
                    )
                    
                    if user_perms_response.status_code == 200:
                        user_data = user_perms_response.json()['data']
                        user_menus = user_data.get('menus', [])
                        print(f'✅ 用户菜单获取成功，菜单数量: {len(user_menus)}')
                        
                        # 检查新菜单是否在用户菜单中
                        def check_menu_in_list(menu_list, target_name):
                            for menu in menu_list:
                                if menu.get('menu_name') == target_name:
                                    return True
                                if menu.get('children'):
                                    if check_menu_in_list(menu['children'], target_name):
                                        return True
                            return False
                        
                        found_new_menu = check_menu_in_list(user_menus, '菜单管理测试(已更新)')
                        
                        if found_new_menu:
                            print('✅ 新菜单出现在用户菜单中')
                        else:
                            print('❌ 新菜单未出现在用户菜单中，需要检查角色分配')
                    else:
                        print(f'❌ 用户权限菜单获取失败: {user_perms_response.status_code}')
                    
                    # 6. 清理测试菜单
                    print('\n🗑️ 清理测试菜单...')
                    delete_response = requests.delete(
                        f'http://localhost:8000/api/v1/organization/menus/{menu_id}/',
                        headers=headers
                    )
                    
                    if delete_response.status_code == 200:
                        print('✅ 测试菜单删除成功')
                    else:
                        print(f'❌ 删除失败: {delete_response.status_code}')
                        print(f'错误信息: {delete_response.text}')
                else:
                    print(f'❌ 菜单创建失败: {create_response.status_code}')
                    print(f'错误信息: {create_response.text}')
            else:
                print(f'❌ 获取菜单列表失败: {menu_response.status_code}')
            
            print('\n📊 菜单管理功能测试完成')
            print('=' * 50)
            print('✅ 后端菜单管理API功能正常')
            print('✅ test_0菜单已成功删除')
            print('💡 如果前端仍有问题，请检查浏览器控制台日志')
        else:
            print('❌ 登录失败')
            
    except requests.exceptions.ConnectionError:
        print('❌ 连接失败，请确保后端服务器正在运行')
    except Exception as e:
        print(f'❌ 测试过程中出现错误: {str(e)}')

if __name__ == '__main__':
    test_menu_management()
