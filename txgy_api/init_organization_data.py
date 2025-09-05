#!/usr/bin/env python
"""
初始化组织架构数据脚本
"""
import os
import django
import uuid

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from apps.organization.models import Role, Permission, Menu, RolePermission, RoleMenu, UserRole

User = get_user_model()

def create_permissions():
    """创建权限数据"""
    permissions_data = [
        # 用户管理权限
        {'perm_code': 'user.view', 'perm_name': '查看用户', 'module': '用户管理', 'function': '用户列表', 'action': 'view', 'api_path': '/api/v1/auth/users/', 'api_method': 'GET'},
        {'perm_code': 'user.create', 'perm_name': '创建用户', 'module': '用户管理', 'function': '用户创建', 'action': 'create', 'api_path': '/api/v1/auth/users/', 'api_method': 'POST'},
        {'perm_code': 'user.edit', 'perm_name': '编辑用户', 'module': '用户管理', 'function': '用户编辑', 'action': 'edit', 'api_path': '/api/v1/auth/users/*/', 'api_method': 'PUT'},
        {'perm_code': 'user.delete', 'perm_name': '删除用户', 'module': '用户管理', 'function': '用户删除', 'action': 'delete', 'api_path': '/api/v1/auth/users/*/', 'api_method': 'DELETE'},
        
        # 角色管理权限
        {'perm_code': 'role.view', 'perm_name': '查看角色', 'module': '角色管理', 'function': '角色列表', 'action': 'view', 'api_path': '/api/v1/organization/roles/', 'api_method': 'GET'},
        {'perm_code': 'role.create', 'perm_name': '创建角色', 'module': '角色管理', 'function': '角色创建', 'action': 'create', 'api_path': '/api/v1/organization/roles/', 'api_method': 'POST'},
        {'perm_code': 'role.edit', 'perm_name': '编辑角色', 'module': '角色管理', 'function': '角色编辑', 'action': 'edit', 'api_path': '/api/v1/organization/roles/*/', 'api_method': 'PUT'},
        {'perm_code': 'role.delete', 'perm_name': '删除角色', 'module': '角色管理', 'function': '角色删除', 'action': 'delete', 'api_path': '/api/v1/organization/roles/*/', 'api_method': 'DELETE'},
        
        # 权限管理权限
        {'perm_code': 'permission.view', 'perm_name': '查看权限', 'module': '权限管理', 'function': '权限列表', 'action': 'view', 'api_path': '/api/v1/organization/permissions/', 'api_method': 'GET'},
        {'perm_code': 'permission.assign', 'perm_name': '分配权限', 'module': '权限管理', 'function': '权限分配', 'action': 'edit', 'api_path': '/api/v1/organization/assign/permissions/', 'api_method': 'POST'},
        
        # 菜单管理权限
        {'perm_code': 'menu.view', 'perm_name': '查看菜单', 'module': '菜单管理', 'function': '菜单列表', 'action': 'view', 'api_path': '/api/v1/organization/menus/tree/', 'api_method': 'GET'},
        {'perm_code': 'menu.assign', 'perm_name': '分配菜单', 'module': '菜单管理', 'function': '菜单分配', 'action': 'edit', 'api_path': '/api/v1/organization/assign/menus/', 'api_method': 'POST'},
        
        # 系统管理权限
        {'perm_code': 'system.config', 'perm_name': '系统配置', 'module': '系统管理', 'function': '系统配置', 'action': 'edit', 'api_path': '/api/v1/organization/configs/', 'api_method': 'GET'},
        {'perm_code': 'system.logs', 'perm_name': '操作日志', 'module': '系统管理', 'function': '操作日志', 'action': 'view', 'api_path': '/api/v1/organization/logs/', 'api_method': 'GET'},
    ]
    
    created_permissions = []
    for perm_data in permissions_data:
        permission, created = Permission.objects.get_or_create(
            perm_code=perm_data['perm_code'],
            defaults=perm_data
        )
        if created:
            created_permissions.append(permission)
    
    print(f"✅ 创建了 {len(created_permissions)} 个权限")
    return Permission.objects.all()

def create_menus():
    """创建菜单数据"""
    menus_data = [
        # 一级菜单
        {'menu_name': '系统管理', 'path': '/admin', 'icon': 'Setting', 'sort': 1, 'parent_id': None},
        {'menu_name': '用户管理', 'path': '/admin/users', 'icon': 'User', 'sort': 2, 'parent_id': None},
        {'menu_name': '内容管理', 'path': '/admin/content', 'icon': 'Document', 'sort': 3, 'parent_id': None},
        {'menu_name': '数据统计', 'path': '/admin/statistics', 'icon': 'DataBoard', 'sort': 4, 'parent_id': None},
    ]
    
    # 创建一级菜单
    parent_menus = {}
    for menu_data in menus_data:
        menu, created = Menu.objects.get_or_create(
            path=menu_data['path'],
            defaults=menu_data
        )
        parent_menus[menu_data['menu_name']] = menu
    
    # 二级菜单
    sub_menus_data = [
        # 系统管理子菜单
        {'menu_name': '角色管理', 'path': '/admin/roles', 'icon': 'UserFilled', 'sort': 1, 'parent': '系统管理', 'component': 'admin/Roles'},
        {'menu_name': '权限管理', 'path': '/admin/permissions', 'icon': 'Lock', 'sort': 2, 'parent': '系统管理', 'component': 'admin/Permissions'},
        {'menu_name': '系统设置', 'path': '/admin/settings', 'icon': 'Tools', 'sort': 4, 'parent': '系统管理', 'component': 'admin/Settings'},

        # 用户管理子菜单
        {'menu_name': '用户列表', 'path': '/admin/users', 'icon': 'User', 'sort': 1, 'parent': '用户管理', 'component': 'admin/Users'},
    ]
    
    created_menus = []
    for menu_data in sub_menus_data:
        parent_menu = parent_menus.get(menu_data['parent'])
        if parent_menu:
            menu_data['parent_id'] = parent_menu.menu_id
            del menu_data['parent']
            
            menu, created = Menu.objects.get_or_create(
                path=menu_data['path'],
                defaults=menu_data
            )
            if created:
                created_menus.append(menu)
    
    print(f"✅ 创建了 {len(created_menus)} 个菜单")
    return Menu.objects.all()

def create_roles():
    """创建角色数据"""
    roles_data = [
        {'role_name': '超级管理员', 'description': '拥有系统所有权限', 'is_default': True},
        {'role_name': '系统管理员', 'description': '负责系统配置和用户管理'},
        {'role_name': '内容管理员', 'description': '负责内容审核和发布管理'},
        {'role_name': '普通用户', 'description': '基础用户权限', 'is_default': True},
    ]
    
    created_roles = []
    for role_data in roles_data:
        role, created = Role.objects.get_or_create(
            role_name=role_data['role_name'],
            defaults=role_data
        )
        if created:
            created_roles.append(role)
    
    print(f"✅ 创建了 {len(created_roles)} 个角色")
    return Role.objects.all()

def assign_permissions_to_roles():
    """为角色分配权限"""
    # 超级管理员拥有所有权限
    super_admin_role = Role.objects.get(role_name='超级管理员')
    all_permissions = Permission.objects.all()
    
    for permission in all_permissions:
        RolePermission.objects.get_or_create(
            role=super_admin_role,
            permission=permission
        )
    
    # 系统管理员权限
    system_admin_role = Role.objects.get(role_name='系统管理员')
    system_permissions = Permission.objects.filter(
        module__in=['用户管理', '角色管理', '权限管理', '菜单管理', '系统管理']
    )
    
    for permission in system_permissions:
        RolePermission.objects.get_or_create(
            role=system_admin_role,
            permission=permission
        )
    
    print("✅ 权限分配完成")

def assign_menus_to_roles():
    """为角色分配菜单"""
    # 超级管理员拥有所有菜单
    super_admin_role = Role.objects.get(role_name='超级管理员')
    all_menus = Menu.objects.all()
    
    for menu in all_menus:
        RoleMenu.objects.get_or_create(
            role=super_admin_role,
            menu=menu
        )
    
    # 系统管理员菜单
    system_admin_role = Role.objects.get(role_name='系统管理员')
    system_menus = Menu.objects.filter(
        path__in=['/admin', '/admin/users', '/admin/roles', '/admin/permissions', 
                 '/admin/menus', '/admin/configs', '/admin/logs', '/admin/users/list', 
                 '/admin/users/enterprise']
    )
    
    for menu in system_menus:
        RoleMenu.objects.get_or_create(
            role=system_admin_role,
            menu=menu
        )
    
    print("✅ 菜单分配完成")

def assign_admin_role():
    """为管理员用户分配角色"""
    try:
        admin_user = User.objects.get(username='admin')
        super_admin_role = Role.objects.get(role_name='超级管理员')
        
        UserRole.objects.get_or_create(
            user=admin_user,
            role=super_admin_role
        )
        
        print("✅ 管理员角色分配完成")
    except User.DoesNotExist:
        print("❌ 管理员用户不存在，请先创建管理员用户")

def main():
    """主函数"""
    print("🚀 开始初始化组织架构数据...")
    print("=" * 50)
    
    try:
        # 创建权限
        create_permissions()
        
        # 创建菜单
        create_menus()
        
        # 创建角色
        create_roles()
        
        # 分配权限给角色
        assign_permissions_to_roles()
        
        # 分配菜单给角色
        assign_menus_to_roles()
        
        # 为管理员分配角色
        assign_admin_role()
        
        print("\n" + "=" * 50)
        print("🎉 组织架构数据初始化完成！")
        
        # 统计信息
        print(f"\n📊 数据统计:")
        print(f"- 权限数量: {Permission.objects.count()}")
        print(f"- 菜单数量: {Menu.objects.count()}")
        print(f"- 角色数量: {Role.objects.count()}")
        print(f"- 用户角色关联: {UserRole.objects.count()}")
        
    except Exception as e:
        print(f"❌ 初始化失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
