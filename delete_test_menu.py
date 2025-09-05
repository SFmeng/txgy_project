#!/usr/bin/env python3
"""
删除test_0菜单并检查菜单管理功能
"""
import requests

def delete_test_menu():
    print('🔍 查找并删除test_0菜单...')
    print('=' * 50)
    
    # 登录获取token
    login_data = {'username': 'admin', 'password': 'admin123456'}
    
    try:
        login_response = requests.post('http://localhost:8000/api/v1/auth/login/', json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json()['data']['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            print('✅ 登录成功')
            
            # 获取所有菜单，查找test_0
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
                    menu_name = test_menu.get('menu_name', '')
                    menu_id = test_menu.get('menu_id', '')
                    print(f'✅ 找到test_0菜单: {menu_name} (ID: {menu_id})')
                    
                    # 删除菜单
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
                    print('ℹ️ 没有找到test_0菜单')
                    
                    # 显示所有菜单供参考
                    print('\n📋 当前所有菜单:')
                    def show_menus(menu_list, indent=0):
                        for menu in menu_list:
                            prefix = '  ' * indent + ('├── ' if indent > 0 else '└── ')
                            menu_name = menu.get('menu_name', '')
                            menu_id = menu.get('menu_id', '')
                            print(f'{prefix}{menu_name} (ID: {menu_id})')
                            if menu.get('children'):
                                show_menus(menu['children'], indent + 1)
                    
                    show_menus(menus)
                    
                    # 查找包含test的菜单
                    print('\n🔍 查找包含"test"的菜单:')
                    def find_test_menus(menu_list, results=None):
                        if results is None:
                            results = []
                        for menu in menu_list:
                            menu_name = menu.get('menu_name', '').lower()
                            if 'test' in menu_name:
                                results.append(menu)
                            if menu.get('children'):
                                find_test_menus(menu['children'], results)
                        return results
                    
                    test_menus = find_test_menus(menus)
                    if test_menus:
                        for menu in test_menus:
                            menu_name = menu.get('menu_name', '')
                            menu_id = menu.get('menu_id', '')
                            print(f'   - {menu_name} (ID: {menu_id})')
                            
                            # 删除找到的测试菜单
                            delete_response = requests.delete(
                                f'http://localhost:8000/api/v1/organization/menus/{menu_id}/',
                                headers=headers
                            )
                            
                            if delete_response.status_code == 200:
                                print(f'     ✅ 删除成功')
                            else:
                                print(f'     ❌ 删除失败: {delete_response.status_code}')
                    else:
                        print('   没有找到包含"test"的菜单')
            else:
                print(f'❌ 获取菜单失败: {menu_response.status_code}')
        else:
            print('❌ 登录失败')
            
    except requests.exceptions.ConnectionError:
        print('❌ 连接失败，请确保后端服务器正在运行')
    except Exception as e:
        print(f'❌ 操作过程中出现错误: {str(e)}')

if __name__ == '__main__':
    delete_test_menu()
