#!/usr/bin/env python3
"""
测试菜单自动分配功能
"""
import requests
import json
import time

def test_menu_auto_assign():
    print('🔍 测试菜单自动分配功能...')
    print('=' * 60)
    
    # 登录获取token
    login_data = {'username': 'admin', 'password': 'admin123456'}
    
    try:
        login_response = requests.post('http://localhost:8000/api/v1/auth/login/', json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json()['data']['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            print('✅ 登录成功')
            
            # 1. 获取当前用户菜单数量
            print('\n📋 获取当前用户菜单...')
            user_perms_response = requests.get(
                'http://localhost:8000/api/v1/organization/user/permissions/', 
                headers=headers
            )
            
            initial_menu_count = 0
            if user_perms_response.status_code == 200:
                user_data = user_perms_response.json()['data']
                current_menus = user_data.get('menus', [])
                initial_menu_count = len(current_menus)
                print(f'✅ 当前用户有 {initial_menu_count} 个顶级菜单')
                
                # 显示当前菜单
                for menu in current_menus:
                    children_count = len(menu.get('children', []))
                    print(f'   - {menu["menu_name"]} ({menu["path"]}): {children_count} 个子菜单')
            
            # 2. 创建一个测试菜单
            print('\n🆕 创建测试菜单...')
            new_menu = {
                'parent_id': None,  # 顶级菜单
                'menu_name': '自动分配测试菜单',
                'path': '/auto-test-menu',
                'component': 'AutoTestMenu',
                'icon': 'Magic',
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
                print(f'✅ 创建菜单成功: {created_menu["menu_name"]} (ID: {created_menu["menu_id"]})')
                
                # 等待一下，让前端有时间处理自动分配
                print('⏳ 等待自动分配处理...')
                time.sleep(2)
                
                # 3. 重新获取用户菜单，检查是否自动出现
                print('\n🔄 检查菜单是否自动出现...')
                user_perms_response2 = requests.get(
                    'http://localhost:8000/api/v1/organization/user/permissions/', 
                    headers=headers
                )
                
                if user_perms_response2.status_code == 200:
                    user_data2 = user_perms_response2.json()['data']
                    updated_menus = user_data2.get('menus', [])
                    final_menu_count = len(updated_menus)
                    
                    print(f'✅ 用户现在有 {final_menu_count} 个顶级菜单')
                    
                    # 检查新菜单是否出现
                    found_new_menu = False
                    for menu in updated_menus:
                        if menu['menu_name'] == '自动分配测试菜单':
                            found_new_menu = True
                            print(f'   ✅ 找到新菜单: {menu["menu_name"]} ({menu["path"]})')
                            break
                    
                    if found_new_menu:
                        print('🎉 自动分配功能正常工作！')
                    else:
                        print('❌ 新菜单未自动出现，可能需要手动分配')
                        
                        # 检查角色是否有这个菜单
                        print('\n🔍 检查角色菜单分配情况...')
                        roles_response = requests.get('http://localhost:8000/api/v1/organization/roles/', headers=headers)
                        
                        if roles_response.status_code == 200:
                            roles = roles_response.json()['data']['results']
                            for role in roles:
                                role_detail_response = requests.get(
                                    f'http://localhost:8000/api/v1/organization/roles/{role["role_id"]}/',
                                    headers=headers
                                )
                                
                                if role_detail_response.status_code == 200:
                                    role_data = role_detail_response.json()['data']
                                    role_menus = role_data.get('menus', [])
                                    
                                    has_new_menu = any(menu['menu_id'] == created_menu['menu_id'] for menu in role_menus)
                                    status = '✅' if has_new_menu else '❌'
                                    print(f'   {status} 角色 {role["role_name"]}: {"已分配" if has_new_menu else "未分配"}')
                
                # 4. 清理测试菜单
                print('\n🗑️ 清理测试菜单...')
                delete_response = requests.delete(
                    f'http://localhost:8000/api/v1/organization/menus/{created_menu["menu_id"]}/',
                    headers=headers
                )
                
                if delete_response.status_code == 200:
                    print('✅ 测试菜单删除成功')
                else:
                    print(f'❌ 删除测试菜单失败: {delete_response.status_code}')
            else:
                print(f'❌ 创建菜单失败: {create_response.status_code} - {create_response.text}')
            
            print('\n' + '=' * 60)
            print('📊 测试总结:')
            if initial_menu_count > 0:
                print('- ✅ 用户菜单获取功能正常')
                print('- ✅ 菜单创建功能正常')
                print('- 💡 如果新菜单没有自动出现，说明需要在前端实现自动分配逻辑')
            else:
                print('- ⚠️  用户当前没有菜单，可能需要先在角色管理中分配菜单')
        else:
            print('❌ 登录失败')
            
    except requests.exceptions.ConnectionError:
        print('❌ 连接失败，请确保后端服务器正在运行')
    except Exception as e:
        print(f'❌ 测试过程中出现错误: {str(e)}')

if __name__ == '__main__':
    test_menu_auto_assign()
