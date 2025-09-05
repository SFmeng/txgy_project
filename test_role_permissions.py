#!/usr/bin/env python3
"""
测试角色权限自动勾选功能
"""
import requests

def test_role_permissions():
    print('🧪 测试角色权限自动勾选功能...')
    print('=' * 50)
    
    # 登录获取token
    login_data = {'username': 'admin', 'password': 'admin123456'}
    login_response = requests.post('http://localhost:8000/api/v1/auth/login/', json=login_data)

    if login_response.status_code == 200:
        token = login_response.json()['data']['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # 获取角色列表
        roles_response = requests.get('http://localhost:8000/api/v1/organization/roles/', headers=headers)
        if roles_response.status_code == 200:
            roles = roles_response.json()['data']['results']
            
            if roles:
                # 测试第一个角色的详情
                first_role = roles[0]
                role_id = first_role['role_id']
                role_name = first_role['role_name']
                
                print(f'测试角色: {role_name}')
                
                role_detail_response = requests.get(
                    f'http://localhost:8000/api/v1/organization/roles/{role_id}/',
                    headers=headers
                )
                
                if role_detail_response.status_code == 200:
                    role_detail = role_detail_response.json()['data']
                    permissions = role_detail.get('permissions', [])
                    menus = role_detail.get('menus', [])
                    
                    print(f'✅ 角色详情获取成功')
                    print(f'   - 权限数量: {len(permissions)}')
                    print(f'   - 菜单数量: {len(menus)}')
                    
                    if permissions:
                        print('   - 权限列表:')
                        for perm in permissions[:3]:  # 只显示前3个
                            perm_name = perm.get('perm_name', '')
                            perm_id = perm.get('perm_id', '')
                            print(f'     * {perm_name} ({perm_id})')
                    
                    if menus:
                        print('   - 菜单列表:')
                        for menu in menus[:3]:  # 只显示前3个
                            menu_name = menu.get('menu_name', '')
                            menu_id = menu.get('menu_id', '')
                            print(f'     * {menu_name} ({menu_id})')
                    
                    # 测试权限树API
                    print('\n🌲 测试权限树API...')
                    perm_tree_response = requests.get(
                        'http://localhost:8000/api/v1/organization/permissions/manage/?group_by_module=true',
                        headers=headers
                    )
                    
                    if perm_tree_response.status_code == 200:
                        perm_modules = perm_tree_response.json()['data']
                        print(f'✅ 权限树获取成功，模块数量: {len(perm_modules)}')

                        if perm_modules:
                            first_module = list(perm_modules.keys())[0]
                            permissions = perm_modules[first_module]
                            print(f'   - 示例模块: {first_module}')
                            print(f'   - 权限数量: {len(permissions)}')
                    else:
                        print(f'❌ 权限树获取失败: {perm_tree_response.status_code}')
                    
                    # 测试菜单树API
                    print('\n🌲 测试菜单树API...')
                    menu_tree_response = requests.get(
                        'http://localhost:8000/api/v1/organization/menus/tree/',
                        headers=headers
                    )
                    
                    if menu_tree_response.status_code == 200:
                        menu_tree = menu_tree_response.json()['data']
                        print(f'✅ 菜单树获取成功，节点数量: {len(menu_tree)}')
                        
                        if menu_tree:
                            first_node = menu_tree[0]
                            print(f'   - 示例节点: {first_node.get("menu_name")}')
                            children = first_node.get('children', [])
                            print(f'   - 子节点数量: {len(children)}')
                    else:
                        print(f'❌ 菜单树获取失败: {menu_tree_response.status_code}')
                    
                else:
                    print(f'❌ 获取角色详情失败: {role_detail_response.status_code}')
            else:
                print('❌ 没有角色数据')
        else:
            print(f'❌ 获取角色列表失败: {roles_response.status_code}')
    else:
        print('❌ 登录失败')

if __name__ == '__main__':
    test_role_permissions()
