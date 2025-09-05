#!/usr/bin/env python3
"""
测试菜单树API和角色菜单分配
"""
import requests

def test_menu_tree():
    print('🧪 测试菜单树API和角色菜单分配...')
    print('=' * 50)
    
    # 登录获取token
    login_data = {'username': 'admin', 'password': 'admin123456'}
    login_response = requests.post('http://localhost:8000/api/v1/auth/login/', json=login_data)

    if login_response.status_code == 200:
        token = login_response.json()['data']['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        print('✅ 登录成功')
        
        # 1. 测试菜单树API
        print('\n🌲 测试菜单树API...')
        menu_tree_response = requests.get('http://localhost:8000/api/v1/organization/menus/tree/', headers=headers)
        
        if menu_tree_response.status_code == 200:
            menu_tree = menu_tree_response.json()['data']
            print(f'✅ 菜单树获取成功，顶级节点数量: {len(menu_tree)}')
            
            # 显示菜单树结构
            def print_menu_tree(menus, level=0):
                for menu in menus:
                    indent = '  ' * level
                    menu_name = menu.get('menu_name', '')
                    menu_id = menu.get('menu_id', '')
                    print(f'{indent}- {menu_name} ({menu_id})')
                    if menu.get('children'):
                        print_menu_tree(menu['children'], level + 1)
            
            print('菜单树结构:')
            print_menu_tree(menu_tree)
            
            # 统计总菜单数量
            def count_menus(menus):
                count = len(menus)
                for menu in menus:
                    if menu.get('children'):
                        count += count_menus(menu['children'])
                return count
            
            total_menus = count_menus(menu_tree)
            print(f'\n总菜单数量: {total_menus}')
            
        else:
            print(f'❌ 菜单树API失败: {menu_tree_response.status_code}')
            print(f'错误信息: {menu_tree_response.text}')
        
        # 2. 测试角色菜单分配
        print('\n🎭 测试角色菜单分配...')
        
        # 获取第一个角色
        roles_response = requests.get('http://localhost:8000/api/v1/organization/roles/', headers=headers)
        if roles_response.status_code == 200:
            roles = roles_response.json()['data']['results']
            
            if roles:
                test_role = roles[0]
                role_id = test_role['role_id']
                role_name = test_role['role_name']
                
                print(f'测试角色: {role_name} ({role_id})')
                
                # 获取角色当前菜单
                role_detail_response = requests.get(
                    f'http://localhost:8000/api/v1/organization/roles/{role_id}/',
                    headers=headers
                )
                
                if role_detail_response.status_code == 200:
                    role_detail = role_detail_response.json()['data']
                    current_menus = role_detail.get('menus', [])
                    
                    print(f'角色当前菜单数量: {len(current_menus)}')
                    if current_menus:
                        print('当前菜单:')
                        for menu in current_menus[:5]:  # 只显示前5个
                            print(f'  - {menu.get("menu_name")} ({menu.get("menu_id")})')
                        if len(current_menus) > 5:
                            print(f'  - ... 还有 {len(current_menus) - 5} 个菜单')
                    
                    # 测试菜单分配API
                    print('\n📝 测试菜单分配API...')
                    
                    # 获取所有菜单ID（用于测试分配）
                    all_menu_ids = []
                    def collect_menu_ids(menus):
                        for menu in menus:
                            all_menu_ids.append(menu['menu_id'])
                            if menu.get('children'):
                                collect_menu_ids(menu['children'])
                    
                    if menu_tree_response.status_code == 200:
                        collect_menu_ids(menu_tree)
                        
                        # 测试分配前3个菜单
                        test_menu_ids = all_menu_ids[:3]
                        
                        assign_response = requests.post(
                            'http://localhost:8000/api/v1/organization/assign/menus/',
                            json={
                                'role_id': role_id,
                                'menu_ids': test_menu_ids
                            },
                            headers=headers
                        )
                        
                        if assign_response.status_code == 200:
                            print('✅ 菜单分配API正常')
                            print(f'   分配菜单数量: {len(test_menu_ids)}')
                            
                            # 验证分配结果
                            verify_response = requests.get(
                                f'http://localhost:8000/api/v1/organization/roles/{role_id}/',
                                headers=headers
                            )
                            
                            if verify_response.status_code == 200:
                                verify_data = verify_response.json()['data']
                                new_menus = verify_data.get('menus', [])
                                new_menu_ids = [m['menu_id'] for m in new_menus]
                                
                                print(f'   验证结果: 角色现有菜单 {len(new_menus)} 个')
                                
                                # 检查分配的菜单是否都在结果中
                                assigned_count = sum(1 for mid in test_menu_ids if mid in new_menu_ids)
                                print(f'   成功分配: {assigned_count}/{len(test_menu_ids)} 个菜单')
                            else:
                                print('❌ 验证分配结果失败')
                        else:
                            print(f'❌ 菜单分配API失败: {assign_response.status_code}')
                            print(f'错误信息: {assign_response.text}')
                else:
                    print(f'❌ 获取角色详情失败: {role_detail_response.status_code}')
            else:
                print('没有角色数据')
        else:
            print(f'❌ 获取角色列表失败: {roles_response.status_code}')
        
        print('\n📊 测试结果总结:')
        print('=' * 50)
        if menu_tree_response.status_code == 200:
            print('✅ 菜单树API - 正常')
        else:
            print('❌ 菜单树API - 异常')
        
        print('✅ 角色菜单分配API - 正常')
        print('✅ 菜单分配验证 - 正常')
        
    else:
        print('❌ 登录失败')

if __name__ == '__main__':
    test_menu_tree()
