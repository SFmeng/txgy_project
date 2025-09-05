"""
组织架构管理后台
"""
from django.contrib import admin
from .models import Role, Permission, Menu, RolePermission, RoleMenu, UserRole, OperationLog, SystemConfig


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """角色管理"""
    list_display = ['role_name', 'description', 'is_default', 'is_active', 'create_time']
    list_filter = ['is_default', 'is_active', 'create_time']
    search_fields = ['role_name', 'description']
    readonly_fields = ['role_id', 'create_time', 'update_time']
    ordering = ['-create_time']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """权限管理"""
    list_display = ['perm_name', 'perm_code', 'module', 'function', 'action', 'is_api']
    list_filter = ['module', 'function', 'action', 'is_api']
    search_fields = ['perm_name', 'perm_code', 'module', 'function']
    readonly_fields = ['perm_id', 'create_time']
    ordering = ['module', 'function', 'action']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """菜单管理"""
    list_display = ['menu_name', 'path', 'parent_id', 'sort', 'terminal', 'is_show', 'is_external']
    list_filter = ['terminal', 'is_show', 'is_external']
    search_fields = ['menu_name', 'path']
    readonly_fields = ['menu_id', 'create_time', 'update_time']
    ordering = ['sort', 'create_time']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """用户角色关联管理"""
    list_display = ['user', 'role', 'create_time']
    list_filter = ['role', 'create_time']
    search_fields = ['user__username', 'user__real_name', 'role__role_name']
    readonly_fields = ['create_time']


@admin.register(OperationLog)
class OperationLogAdmin(admin.ModelAdmin):
    """操作日志管理"""
    list_display = ['user', 'operation', 'module', 'ip_address', 'operation_time', 'operation_result']
    list_filter = ['module', 'operation_result', 'operation_time']
    search_fields = ['user__username', 'operation', 'module']
    readonly_fields = ['log_id', 'operation_time']
    ordering = ['-operation_time']


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    """系统配置管理"""
    list_display = ['config_key', 'config_type', 'description', 'is_active', 'update_time']
    list_filter = ['config_type', 'is_active']
    search_fields = ['config_key', 'description']
    readonly_fields = ['config_id', 'create_time', 'update_time']
    ordering = ['config_type', 'config_key']
