"""
组织架构序列化器
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Role, Permission, Menu, RolePermission, RoleMenu, UserRole, OperationLog, SystemConfig

User = get_user_model()


class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器"""
    
    class Meta:
        model = Permission
        fields = [
            'perm_id', 'perm_code', 'perm_name', 'module', 'function', 
            'action', 'is_api', 'api_path', 'api_method', 'description', 'create_time'
        ]
        read_only_fields = ['perm_id', 'create_time']


class MenuSerializer(serializers.ModelSerializer):
    """菜单序列化器"""
    
    perm_name = serializers.CharField(source='perm.perm_name', read_only=True)
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Menu
        fields = [
            'menu_id', 'parent_id', 'menu_name', 'path', 'component', 
            'icon', 'sort', 'terminal', 'perm', 'perm_name', 'is_show', 
            'is_external', 'children', 'create_time', 'update_time'
        ]
        read_only_fields = ['menu_id', 'create_time', 'update_time']
    
    def get_children(self, obj):
        """获取子菜单"""
        children = Menu.objects.filter(parent_id=obj.menu_id, is_show=True).order_by('sort')
        return MenuSerializer(children, many=True).data


class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器"""

    permissions = serializers.SerializerMethodField()
    menus = serializers.SerializerMethodField()
    user_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = [
            'role_id', 'role_name', 'description', 'is_default', 'is_active',
            'permissions', 'menus', 'user_count', 'create_time', 'update_time'
        ]
        read_only_fields = ['role_id', 'create_time', 'update_time']

    def get_permissions(self, obj):
        """获取角色权限"""
        role_permissions = RolePermission.objects.filter(role=obj).select_related('permission')
        return PermissionSerializer([rp.permission for rp in role_permissions], many=True).data

    def get_menus(self, obj):
        """获取角色菜单"""
        role_menus = RoleMenu.objects.filter(role=obj).select_related('menu')
        return MenuSerializer([rm.menu for rm in role_menus], many=True).data

    def get_user_count(self, obj):
        """获取角色下的用户数量"""
        return UserRole.objects.filter(role=obj).count()


class RolePermissionSerializer(serializers.ModelSerializer):
    """角色权限关联序列化器"""
    
    class Meta:
        model = RolePermission
        fields = ['role', 'permission', 'create_time']
        read_only_fields = ['create_time']


class RoleMenuSerializer(serializers.ModelSerializer):
    """角色菜单关联序列化器"""
    
    class Meta:
        model = RoleMenu
        fields = ['role', 'menu', 'create_time']
        read_only_fields = ['create_time']


class UserRoleSerializer(serializers.ModelSerializer):
    """用户角色关联序列化器"""
    
    role_name = serializers.CharField(source='role.role_name', read_only=True)
    
    class Meta:
        model = UserRole
        fields = ['user', 'role', 'role_name', 'create_time']
        read_only_fields = ['create_time']


class UserManagementSerializer(serializers.ModelSerializer):
    """用户管理序列化器"""
    
    roles = RoleSerializer(many=True, read_only=True)
    role_names = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email', 'phone', 'user_type', 'real_name',
            'avatar', 'status', 'is_active', 'roles', 'role_names',
            'last_login', 'date_joined'
        ]
        read_only_fields = ['user_id', 'date_joined']
    
    def get_role_names(self, obj):
        """获取用户角色名称列表"""
        user_roles = UserRole.objects.filter(user=obj).select_related('role')
        return [ur.role.role_name for ur in user_roles]


class OperationLogSerializer(serializers.ModelSerializer):
    """操作日志序列化器"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    real_name = serializers.CharField(source='user.real_name', read_only=True)
    
    class Meta:
        model = OperationLog
        fields = [
            'log_id', 'user', 'username', 'real_name', 'operation', 'module',
            'ip_address', 'user_agent', 'operation_time', 'operation_result', 'error_msg'
        ]
        read_only_fields = ['log_id', 'operation_time']


class SystemConfigSerializer(serializers.ModelSerializer):
    """系统配置序列化器"""
    
    class Meta:
        model = SystemConfig
        fields = [
            'config_id', 'config_key', 'config_value', 'config_type',
            'description', 'is_active', 'create_time', 'update_time'
        ]
        read_only_fields = ['config_id', 'create_time', 'update_time']


class UserPermissionSerializer(serializers.Serializer):
    """用户权限序列化器"""
    
    permissions = PermissionSerializer(many=True, read_only=True)
    menus = MenuSerializer(many=True, read_only=True)
    user_info = UserManagementSerializer(read_only=True)


class RoleAssignSerializer(serializers.Serializer):
    """角色分配序列化器"""
    
    user_ids = serializers.ListField(
        child=serializers.CharField(),
        help_text="用户ID列表"
    )
    role_ids = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="角色ID列表"
    )


class PermissionAssignSerializer(serializers.Serializer):
    """权限分配序列化器"""
    
    role_id = serializers.UUIDField(help_text="角色ID")
    permission_ids = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="权限ID列表"
    )


class MenuAssignSerializer(serializers.Serializer):
    """菜单分配序列化器"""
    
    role_id = serializers.UUIDField(help_text="角色ID")
    menu_ids = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="菜单ID列表"
    )
