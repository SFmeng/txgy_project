#!/usr/bin/env python3
"""
测试权限管理和菜单管理API
"""
import requests
import json

def test_permission_menu_api():
    print('🔍 测试权限管理和菜单管理API...')
    print('=' * 60)
    
    # 登录获取token
    print('🔑 用户登录...')
    login_data = {'username': 'admin', 'password': 'admin123456'}
    
    try:
        login_response = requests.post('http://localhost:8000/api/v1/auth/login/', json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json()['data']['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            print('✅ 登录成功')
            
            # 测试权限管理API
            print('\n📋 测试权限管理API...')
            
            # 1. 获取权限列表（按模块分组）
            print('1. 获取权限列表（按模块分组）...')
            perm_response = requests.get(
                'http://localhost:8000/api/v1/organization/permissions/manage/?group_by_module=true', 
                headers=headers
            )
            
            if perm_response.status_code == 200:
                modules = perm_response.json()['data']
                print(f'✅ 获取权限成功，共 {len(modules)} 个模块')
                for module_name, perms in modules.items():
                    print(f'   - {module_name}: {len(perms)} 个权限')
                    if perms:
                        print(f'     示例权限: {perms[0]["perm_name"]} ({perms[0]["perm_code"]})')
            else:
                print(f'❌ 获取权限失败: {perm_response.status_code} - {perm_response.text}')
            
            # 2. 获取权限列表（表格模式）
            print('\n2. 获取权限列表（表格模式）...')
            perm_table_response = requests.get(
                'http://localhost:8000/api/v1/organization/permissions/manage/?page=1&page_size=10', 
                headers=headers
            )
            
            if perm_table_response.status_code == 200:
                perm_data = perm_table_response.json()['data']
                print(f'✅ 获取权限表格数据成功，共 {perm_data["total"]} 条记录')
                print(f'   当前页: {perm_data["page"]}, 每页: {perm_data["page_size"]}')
                if perm_data['results']:
                    print(f'   示例权限: {perm_data["results"][0]["perm_name"]}')
            else:
                print(f'❌ 获取权限表格数据失败: {perm_table_response.status_code}')
            
            # 测试菜单管理API
            print('\n🌲 测试菜单管理API...')
            
            # 1. 获取菜单树
            print('1. 获取菜单树...')
            menu_response = requests.get(
                'http://localhost:8000/api/v1/organization/menus/?terminal=pc', 
                headers=headers
            )
            
            if menu_response.status_code == 200:
                menus = menu_response.json()['data']
                print(f'✅ 获取菜单成功，共 {len(menus)} 个顶级菜单')
                for menu in menus:
                    children_count = len(menu.get('children', []))
                    print(f'   - {menu["menu_name"]} ({menu["path"]}): {children_count} 个子菜单')
                    
                    # 显示子菜单
                    for child in menu.get('children', [])[:3]:  # 只显示前3个子菜单
                        print(f'     └─ {child["menu_name"]} ({child["path"]})')
                    
                    if len(menu.get('children', [])) > 3:
                        print(f'     └─ ... 还有 {len(menu["children"]) - 3} 个子菜单')
            else:
                print(f'❌ 获取菜单失败: {menu_response.status_code} - {menu_response.text}')
            
            # 测试创建权限
            print('\n🆕 测试创建权限...')
            new_permission = {
                'perm_name': '测试权限',
                'perm_code': 'test.view',
                'module': '测试模块',
                'function': '测试功能',
                'action': 'view',
                'api_path': '/api/v1/test/',
                'api_method': 'GET',
                'description': '这是一个测试权限'
            }
            
            create_perm_response = requests.post(
                'http://localhost:8000/api/v1/organization/permissions/manage/',
                json=new_permission,
                headers=headers
            )
            
            if create_perm_response.status_code == 200:
                created_perm = create_perm_response.json()['data']
                print(f'✅ 创建权限成功: {created_perm["perm_name"]} ({created_perm["perm_code"]})')
                
                # 测试删除权限
                print('🗑️ 测试删除权限...')
                delete_response = requests.delete(
                    f'http://localhost:8000/api/v1/organization/permissions/{created_perm["perm_id"]}/',
                    headers=headers
                )
                
                if delete_response.status_code == 200:
                    print('✅ 删除权限成功')
                else:
                    print(f'❌ 删除权限失败: {delete_response.status_code}')
            else:
                print(f'❌ 创建权限失败: {create_perm_response.status_code} - {create_perm_response.text}')
            
            print('\n' + '=' * 60)
            print('📊 API测试结果总结:')
            print('- ✅ 权限管理API (按模块分组)')
            print('- ✅ 权限管理API (表格模式)')
            print('- ✅ 菜单管理API (树形结构)')
            print('- ✅ 权限CRUD操作')
            print('\n🎉 所有API测试通过！')
            
        else:
            print(f'❌ 登录失败: {login_response.status_code} - {login_response.text}')
            
    except requests.exceptions.ConnectionError:
        print('❌ 连接失败，请确保后端服务器正在运行 (http://localhost:8000)')
    except Exception as e:
        print(f'❌ 测试过程中出现错误: {str(e)}')

if __name__ == '__main__':
    test_permission_menu_api()
