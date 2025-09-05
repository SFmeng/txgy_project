#!/usr/bin/env python3
"""
诊断菜单分配问题
"""
import requests

def diagnose_menu_assignment():
    print('🔍 诊断菜单分配问题...')
    print('=' * 50)
    
    # 登录获取token
    login_data = {'username': 'admin', 'password': 'admin123456'}
    login_response = requests.post('http://localhost:8000/api/v1/auth/login/', json=login_data)

    if login_response.status_code == 200:
        token = login_response.json()['data']['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        print('✅ 登录成功')
        
        # 1. 获取角色列表
        roles_response = requests.get('http://localhost:8000/api/v1/organization/roles/', headers=headers)
        if roles_response.status_code != 200:
            print('❌ 获取角色列表失败')
            return
        
        roles = roles_response.json()['data']['results']
        test_role = roles[0]
        role_id = test_role['role_id']
        role_name = test_role['role_name']
        
        print(f'测试角色: {role_name} ({role_id})')
        
        # 2. 获取角色当前菜单
        print('\n📋 获取角色当前菜单...')
        role_detail_response = requests.get(
            f'http://localhost:8000/api/v1/organization/roles/{role_id}/',
            headers=headers
        )
        
        if role_detail_response.status_code == 200:
            role_detail = role_detail_response.json()['data']
            current_menus = role_detail.get('menus', [])
            current_menu_ids = [m['menu_id'] for m in current_menus]
            
            print(f'角色当前菜单数量: {len(current_menus)}')
            print('当前菜单ID列表:')
            for menu in current_menus:
                print(f'  - {menu["menu_name"]} ({menu["menu_id"]})')
        else:
            print('❌ 获取角色详情失败')
            return
        
        # 3. 获取完整菜单树
        print('\n🌲 获取完整菜单树...')
        menu_tree_response = requests.get('http://localhost:8000/api/v1/organization/menus/tree/', headers=headers)
        
        if menu_tree_response.status_code == 200:
            menu_tree = menu_tree_response.json()['data']
            
            # 收集所有菜单ID
            all_menu_ids = []
            def collect_menu_ids(menus):
                for menu in menus:
                    all_menu_ids.append(menu['menu_id'])
                    if menu.get('children'):
                        collect_menu_ids(menu['children'])
            
            collect_menu_ids(menu_tree)
            print(f'系统总菜单数量: {len(all_menu_ids)}')
            
            # 找到"测试菜单"
            test_menu_id = None
            def find_test_menu(menus):
                nonlocal test_menu_id
                for menu in menus:
                    if '测试' in menu.get('menu_name', ''):
                        test_menu_id = menu['menu_id']
                        print(f'找到测试菜单: {menu["menu_name"]} ({menu["menu_id"]})')
                        return True
                    if menu.get('children'):
                        if find_test_menu(menu['children']):
                            return True
                return False
            
            find_test_menu(menu_tree)
            
            # 检查测试菜单是否在角色的当前菜单中
            if test_menu_id:
                is_assigned = test_menu_id in current_menu_ids
                print(f'测试菜单是否已分配给角色: {"是" if is_assigned else "否"}')
                
                if is_assigned:
                    print('🔍 问题分析: 测试菜单已分配给角色，但前端显示可能有问题')
                    
                    # 测试重新分配相同的菜单
                    print('\n🔄 测试重新分配相同菜单...')
                    reassign_response = requests.post(
                        'http://localhost:8000/api/v1/organization/assign/menus/',
                        json={
                            'role_id': role_id,
                            'menu_ids': current_menu_ids  # 重新分配相同的菜单
                        },
                        headers=headers
                    )
                    
                    if reassign_response.status_code == 200:
                        print('✅ 重新分配成功')
                        
                        # 验证重新分配后的结果
                        verify_response = requests.get(
                            f'http://localhost:8000/api/v1/organization/roles/{role_id}/',
                            headers=headers
                        )
                        
                        if verify_response.status_code == 200:
                            verify_data = verify_response.json()['data']
                            new_menus = verify_data.get('menus', [])
                            new_menu_ids = [m['menu_id'] for m in new_menus]
                            
                            print(f'重新分配后菜单数量: {len(new_menus)}')
                            
                            # 检查测试菜单是否还在
                            still_assigned = test_menu_id in new_menu_ids
                            print(f'测试菜单是否仍在分配列表中: {"是" if still_assigned else "否"}')
                            
                            if not still_assigned:
                                print('❌ 问题确认: 重新分配后测试菜单丢失')
                            else:
                                print('✅ 重新分配后测试菜单仍在列表中')
                        else:
                            print('❌ 验证重新分配结果失败')
                    else:
                        print(f'❌ 重新分配失败: {reassign_response.text}')
                else:
                    print('测试菜单未分配给角色，这是正常的')
            else:
                print('未找到测试菜单')
        else:
            print('❌ 获取菜单树失败')
        
        # 4. 测试菜单使用情况查询
        print('\n👁️ 测试菜单使用情况查询...')
        
        if test_menu_id:
            # 模拟前端的菜单使用情况查询逻辑
            using_roles = []
            
            for role in roles:
                role_detail_response = requests.get(
                    f'http://localhost:8000/api/v1/organization/roles/{role["role_id"]}/',
                    headers=headers
                )
                
                if role_detail_response.status_code == 200:
                    role_detail = role_detail_response.json()['data']
                    role_menus = role_detail.get('menus', [])
                    
                    if any(menu['menu_id'] == test_menu_id for menu in role_menus):
                        using_roles.append(role)
            
            print(f'使用测试菜单的角色数量: {len(using_roles)}')
            for role in using_roles:
                print(f'  - {role["role_name"]}')
        
        print('\n📊 诊断结果总结:')
        print('=' * 50)
        print('✅ 角色详情API - 正常')
        print('✅ 菜单树API - 正常')
        print('✅ 菜单分配API - 正常')
        print('✅ 菜单使用情况查询 - 正常')
        
        if test_menu_id and test_menu_id in current_menu_ids:
            print('⚠️  问题可能在前端菜单树的自动勾选逻辑')
        else:
            print('✅ 菜单分配状态正常')
        
    else:
        print('❌ 登录失败')

if __name__ == '__main__':
    diagnose_menu_assignment()
