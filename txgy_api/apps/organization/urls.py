"""
组织架构URL配置
"""
from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    # 角色管理
    path('roles/', views.role_list, name='role_list'),
    path('roles/<uuid:role_id>/', views.role_detail, name='role_detail'),
    
    # 权限管理
    path('permissions/', views.permission_list, name='permission_list'),
    path('permissions/manage/', views.permission_management, name='permission_management'),
    path('permissions/<str:perm_id>/', views.permission_detail, name='permission_detail'),

    # 菜单管理
    path('menus/tree/', views.menu_tree, name='menu_tree'),
    path('menus/', views.menu_management, name='menu_management'),
    path('menus/<str:menu_id>/', views.menu_detail, name='menu_detail'),
    
    # 用户权限
    path('user/permissions/', views.user_permissions, name='user_permissions'),
    
    # 角色分配
    path('assign/roles/', views.assign_roles, name='assign_roles'),
    path('assign/permissions/', views.assign_permissions, name='assign_permissions'),
    path('assign/menus/', views.assign_menus, name='assign_menus'),
    
    # 操作日志
    path('logs/', views.operation_logs, name='operation_logs'),
    
    # 系统配置
    path('configs/', views.system_configs, name='system_configs'),
    path('configs/<uuid:config_id>/', views.update_system_config, name='update_system_config'),
]
