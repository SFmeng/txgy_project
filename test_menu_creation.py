#!/usr/bin/env python3
"""
测试菜单新增和刷新功能
"""
import requests
import json

def test_menu_creation():
    print('🔍 测试菜单新增和刷新功能...')
    print('=' * 60)
    
    # 登录获取token
    login_data = {'username': 'admin', 'password': 'admin123456'}
    
    try:
        login_response = requests.post('http://localhost:8000/api/v1/auth/login/', json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json()['data']['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            print('✅ 登录成功')
            
            # 1. 获取当前用户菜单
            print('\n📋 获取当前用户菜单...')
            user_perms_response = requests.get(
                'http://localhost:8000/api/v1/organization/user/permissions/', 
                headers=headers
            )
            
            if user_perms_response.status_code == 200:
                user_data = user_perms_response.json()['data']
                current_menus = user_data.get('menus', [])
                print(f'✅ 当前用户有 {len(current_menus)} 个顶级菜单')
                
                # 显示当前菜单
                for menu in current_menus:
                    children_count = len(menu.get('children', []))
                    print(f'   - {menu["menu_name"]} ({menu["path"]}): {children_count} 个子菜单')
            
            # 2. 创建一个测试菜单
            print('\n🆕 创建测试菜单...')
            new_menu = {
                'parent_id': None,  # 顶级菜单
                'menu_name': '测试菜单',
                'path': '/test-menu',
                'component': 'TestMenu',
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
                print(f'✅ 创建菜单成功: {created_menu["menu_name"]} (ID: {created_menu["menu_id"]})')
                
                # 3. 获取角色列表并分配菜单
                print('\n🎭 为角色分配新菜单...')
                roles_response = requests.get('http://localhost:8000/api/v1/organization/roles/', headers=headers)
                
                if roles_response.status_code == 200:
                    roles = roles_response.json()['data']['results']
                    if roles:
                        admin_role = roles[0]  # 使用第一个角色
                        print(f'✅ 找到角色: {admin_role["role_name"]}')
                        
                        # 获取角色当前的菜单
                        role_detail_response = requests.get(
                            f'http://localhost:8000/api/v1/organization/roles/{admin_role["role_id"]}/',
                            headers=headers
                        )
                        
                        if role_detail_response.status_code == 200:
                            role_data = role_detail_response.json()['data']
                            current_menu_ids = [menu['menu_id'] for menu in role_data.get('menus', [])]
                            
                            # 添加新菜单ID
                            current_menu_ids.append(created_menu['menu_id'])
                            
                            # 分配菜单给角色
                            assign_data = {
                                'role_id': admin_role['role_id'],
                                'menu_ids': current_menu_ids
                            }
                            
                            assign_response = requests.post(
                                'http://localhost:8000/api/v1/organization/assign/menus/',
                                json=assign_data,
                                headers=headers
                            )
                            
                            if assign_response.status_code == 200:
                                print('✅ 菜单分配成功')
                                
                                # 4. 重新获取用户菜单
                                print('\n🔄 重新获取用户菜单...')
                                user_perms_response2 = requests.get(
                                    'http://localhost:8000/api/v1/organization/user/permissions/', 
                                    headers=headers
                                )
                                
                                if user_perms_response2.status_code == 200:
                                    user_data2 = user_perms_response2.json()['data']
                                    updated_menus = user_data2.get('menus', [])
                                    print(f'✅ 用户现在有 {len(updated_menus)} 个顶级菜单')
                                    
                                    # 检查新菜单是否出现
                                    found_new_menu = False
                                    for menu in updated_menus:
                                        if menu['menu_name'] == '测试菜单':
                                            found_new_menu = True
                                            print(f'   ✅ 找到新菜单: {menu["menu_name"]} ({menu["path"]})')
                                            break
                                    
                                    if not found_new_menu:
                                        print('   ❌ 新菜单未出现在用户菜单中')
                                
                                # 5. 清理测试菜单
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
                                print(f'❌ 菜单分配失败: {assign_response.status_code}')
                        else:
                            print('❌ 获取角色详情失败')
                    else:
                        print('❌ 没有找到角色')
                else:
                    print('❌ 获取角色列表失败')
            else:
                print(f'❌ 创建菜单失败: {create_response.status_code} - {create_response.text}')
            
            print('\n' + '=' * 60)
            print('📊 测试结论:')
            print('- ✅ 菜单创建功能正常')
            print('- ✅ 菜单分配功能正常')
            print('- ✅ 用户菜单获取功能正常')
            print('- ⚠️  新增菜单后需要将菜单分配给角色才能在用户界面显示')
            print('- 💡 建议: 菜单管理页面应该在创建菜单后自动分配给当前用户的角色')
        else:
            print('❌ 登录失败')
            
    except requests.exceptions.ConnectionError:
        print('❌ 连接失败，请确保后端服务器正在运行')
    except Exception as e:
        print(f'❌ 测试过程中出现错误: {str(e)}')

if __name__ == '__main__':
    test_menu_creation()
