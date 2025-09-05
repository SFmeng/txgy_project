#!/usr/bin/env python
"""
初始化权限系统脚本
创建基础角色、权限和菜单数据
"""
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from apps.organization.models import Role, Permission, Menu, UserRole, RolePermission, RoleMenu

User = get_user_model()

def create_permissions():
    """创建基础权限"""
    permissions_data = [
        # 用户管理权限
        {'perm_name': '查看用户', 'perm_code': 'user.view', 'module': '用户管理', 'function': '用户列表', 'action': 'view'},
        {'perm_name': '创建用户', 'perm_code': 'user.create', 'module': '用户管理', 'function': '用户创建', 'action': 'create'},
        {'perm_name': '编辑用户', 'perm_code': 'user.edit', 'module': '用户管理', 'function': '用户编辑', 'action': 'edit'},
        {'perm_name': '删除用户', 'perm_code': 'user.delete', 'module': '用户管理', 'function': '用户删除', 'action': 'delete'},
        
        # 角色管理权限
        {'perm_name': '查看角色', 'perm_code': 'role.view', 'module': '角色管理', 'function': '角色列表', 'action': 'view'},
        {'perm_name': '创建角色', 'perm_code': 'role.create', 'module': '角色管理', 'function': '角色创建', 'action': 'create'},
        {'perm_name': '编辑角色', 'perm_code': 'role.edit', 'module': '角色管理', 'function': '角色编辑', 'action': 'edit'},
        {'perm_name': '删除角色', 'perm_code': 'role.delete', 'module': '角色管理', 'function': '角色删除', 'action': 'delete'},
        {'perm_name': '分配权限', 'perm_code': 'role.assign_permissions', 'module': '角色管理', 'function': '权限分配', 'action': 'assign'},
        
        # 权限管理权限
        {'perm_name': '查看权限', 'perm_code': 'permission.view', 'module': '权限管理', 'function': '权限列表', 'action': 'view'},
        {'perm_name': '创建权限', 'perm_code': 'permission.create', 'module': '权限管理', 'function': '权限创建', 'action': 'create'},
        {'perm_name': '编辑权限', 'perm_code': 'permission.edit', 'module': '权限管理', 'function': '权限编辑', 'action': 'edit'},
        {'perm_name': '删除权限', 'perm_code': 'permission.delete', 'module': '权限管理', 'function': '权限删除', 'action': 'delete'},
        
        # 菜单管理权限
        {'perm_name': '查看菜单', 'perm_code': 'menu.view', 'module': '菜单管理', 'function': '菜单列表', 'action': 'view'},
        {'perm_name': '创建菜单', 'perm_code': 'menu.create', 'module': '菜单管理', 'function': '菜单创建', 'action': 'create'},
        {'perm_name': '编辑菜单', 'perm_code': 'menu.edit', 'module': '菜单管理', 'function': '菜单编辑', 'action': 'edit'},
        {'perm_name': '删除菜单', 'perm_code': 'menu.delete', 'module': '菜单管理', 'function': '菜单删除', 'action': 'delete'},
        
        # 系统管理权限
        {'perm_name': '系统设置', 'perm_code': 'system.settings', 'module': '系统管理', 'function': '系统设置', 'action': 'manage'},
        {'perm_name': '查看日志', 'perm_code': 'system.logs', 'module': '系统管理', 'function': '操作日志', 'action': 'view'},
        {'perm_name': '数据统计', 'perm_code': 'system.stats', 'module': '系统管理', 'function': '数据统计', 'action': 'view'},
        
        # 企业认证权限
        {'perm_name': '企业认证审核', 'perm_code': 'enterprise.verify', 'module': '企业管理', 'function': '企业认证', 'action': 'verify'},
        {'perm_name': '查看企业信息', 'perm_code': 'enterprise.view', 'module': '企业管理', 'function': '企业列表', 'action': 'view'},
        
        # 基础权限
        {'perm_name': '访问管理后台', 'perm_code': 'admin.access', 'module': '基础权限', 'function': '后台访问', 'action': 'access'},
        {'perm_name': '查看仪表盘', 'perm_code': 'dashboard.view', 'module': '基础权限', 'function': '仪表盘', 'action': 'view'},
    ]
    
    created_permissions = []
    for perm_data in permissions_data:
        permission, created = Permission.objects.get_or_create(
            perm_code=perm_data['perm_code'],
            defaults=perm_data
        )
        if created:
            created_permissions.append(permission.perm_name)
            print(f"创建权限: {permission.perm_name}")
    
    return created_permissions

def create_menus():
    """创建基础菜单"""
    menus_data = [
        # 管理后台主菜单
        {'menu_name': '仪表盘', 'path': '/admin/dashboard', 'icon': 'Dashboard', 'sort': 1, 'parent_id': None},
        {'menu_name': '用户管理', 'path': '/admin/users', 'icon': 'User', 'sort': 2, 'parent_id': None},
        {'menu_name': '角色管理', 'path': '/admin/roles', 'icon': 'UserFilled', 'sort': 3, 'parent_id': None},
        {'menu_name': '权限管理', 'path': '/admin/permissions', 'icon': 'Lock', 'sort': 4, 'parent_id': None},
        {'menu_name': '菜单管理', 'path': '/admin/menus', 'icon': 'Menu', 'sort': 5, 'parent_id': None},
        {'menu_name': '企业认证', 'path': '/admin/enterprise-verify', 'icon': 'OfficeBuilding', 'sort': 6, 'parent_id': None},
        {'menu_name': '系统设置', 'path': '/admin/settings', 'icon': 'Setting', 'sort': 7, 'parent_id': None},
        {'menu_name': '操作日志', 'path': '/admin/logs', 'icon': 'Document', 'sort': 8, 'parent_id': None},
        
        # 前台用户菜单
        {'menu_name': '首页', 'path': '/', 'icon': 'House', 'sort': 1, 'parent_id': None, 'terminal': 'user'},
        {'menu_name': '信息发布', 'path': '/info', 'icon': 'Bell', 'sort': 2, 'parent_id': None, 'terminal': 'user'},
        {'menu_name': '搜索匹配', 'path': '/search', 'icon': 'Search', 'sort': 3, 'parent_id': None, 'terminal': 'user'},
        {'menu_name': '沟通交流', 'path': '/communication', 'icon': 'ChatDotRound', 'sort': 4, 'parent_id': None, 'terminal': 'user'},
        {'menu_name': '个人中心', 'path': '/profile', 'icon': 'User', 'sort': 5, 'parent_id': None, 'terminal': 'user'},
    ]
    
    created_menus = []
    for menu_data in menus_data:
        menu_data.setdefault('terminal', 'admin')
        menu_data.setdefault('is_show', True)
        menu_data.setdefault('is_external', False)
        
        menu, created = Menu.objects.get_or_create(
            path=menu_data['path'],
            terminal=menu_data['terminal'],
            defaults=menu_data
        )
        if created:
            created_menus.append(menu.menu_name)
            print(f"创建菜单: {menu.menu_name}")
    
    return created_menus

def create_roles():
    """创建基础角色"""
    roles_data = [
        {
            'role_name': '超级管理员',
            'description': '拥有系统所有权限的管理员角色',
            'is_default': False,
            'is_active': True
        },
        {
            'role_name': '普通管理员',
            'description': '拥有基础管理权限的管理员角色',
            'is_default': False,
            'is_active': True
        },
        {
            'role_name': '企业用户',
            'description': '企业用户默认角色',
            'is_default': True,
            'is_active': True
        },
        {
            'role_name': '个人用户',
            'description': '个人用户默认角色',
            'is_default': True,
            'is_active': True
        }
    ]
    
    created_roles = []
    for role_data in roles_data:
        role, created = Role.objects.get_or_create(
            role_name=role_data['role_name'],
            defaults=role_data
        )
        if created:
            created_roles.append(role.role_name)
            print(f"创建角色: {role.role_name}")
    
    return created_roles

def assign_admin_permissions():
    """为超级管理员分配所有权限"""
    try:
        admin_role = Role.objects.get(role_name='超级管理员')
        all_permissions = Permission.objects.all()
        
        # 清除现有权限关联
        RolePermission.objects.filter(role=admin_role).delete()
        
        # 分配所有权限
        role_permissions = []
        for permission in all_permissions:
            role_permissions.append(RolePermission(role=admin_role, permission=permission))
        
        RolePermission.objects.bulk_create(role_permissions)
        print(f"为超级管理员分配了 {len(role_permissions)} 个权限")
        
        # 分配所有管理菜单
        admin_menus = Menu.objects.filter(terminal='admin')
        RoleMenu.objects.filter(role=admin_role).delete()
        
        role_menus = []
        for menu in admin_menus:
            role_menus.append(RoleMenu(role=admin_role, menu=menu))
        
        RoleMenu.objects.bulk_create(role_menus)
        print(f"为超级管理员分配了 {len(role_menus)} 个菜单")
        
    except Role.DoesNotExist:
        print("超级管理员角色不存在")

def assign_admin_role_to_superuser():
    """为超级用户分配管理员角色"""
    try:
        # 查找超级用户
        superusers = User.objects.filter(is_superuser=True)
        admin_role = Role.objects.get(role_name='超级管理员')
        
        for user in superusers:
            user_role, created = UserRole.objects.get_or_create(
                user=user,
                role=admin_role
            )
            if created:
                print(f"为用户 {user.username} 分配了超级管理员角色")
            else:
                print(f"用户 {user.username} 已经拥有超级管理员角色")
                
    except Role.DoesNotExist:
        print("超级管理员角色不存在")

def main():
    """主函数"""
    print("开始初始化权限系统...")
    
    # 创建权限
    print("\n1. 创建基础权限...")
    create_permissions()
    
    # 创建菜单
    print("\n2. 创建基础菜单...")
    create_menus()
    
    # 创建角色
    print("\n3. 创建基础角色...")
    create_roles()
    
    # 为超级管理员分配权限
    print("\n4. 为超级管理员分配权限...")
    assign_admin_permissions()
    
    # 为超级用户分配管理员角色
    print("\n5. 为超级用户分配管理员角色...")
    assign_admin_role_to_superuser()
    
    print("\n权限系统初始化完成！")

if __name__ == '__main__':
    main()
