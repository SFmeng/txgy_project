"""
组织架构模型
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Role(models.Model):
    """角色模型"""
    
    role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='角色ID')
    role_name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    description = models.TextField(blank=True, null=True, verbose_name='角色描述')
    is_default = models.BooleanField(default=False, verbose_name='是否默认角色')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'tx_roles'
        verbose_name = '角色'
        verbose_name_plural = '角色'
        ordering = ['-create_time']
    
    def __str__(self):
        return self.role_name


class Permission(models.Model):
    """权限模型"""
    
    ACTION_CHOICES = [
        ('view', '查看'),
        ('create', '新增'),
        ('edit', '编辑'),
        ('delete', '删除'),
        ('audit', '审核'),
        ('export', '导出'),
        ('import', '导入'),
    ]
    
    perm_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='权限ID')
    perm_code = models.CharField(max_length=100, unique=True, verbose_name='权限标识')
    perm_name = models.CharField(max_length=50, verbose_name='权限名称')
    module = models.CharField(max_length=50, verbose_name='所属模块')
    function = models.CharField(max_length=50, verbose_name='所属功能')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='操作类型')
    is_api = models.BooleanField(default=True, verbose_name='是否接口权限')
    api_path = models.CharField(max_length=200, blank=True, null=True, verbose_name='接口路径')
    api_method = models.CharField(max_length=10, blank=True, null=True, verbose_name='接口方法')
    description = models.TextField(blank=True, null=True, verbose_name='权限描述')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'tx_permissions'
        verbose_name = '权限'
        verbose_name_plural = '权限'
        ordering = ['module', 'function', 'action']
    
    def __str__(self):
        return f"{self.module}-{self.function}-{self.perm_name}"


class Menu(models.Model):
    """菜单模型"""
    
    TERMINAL_CHOICES = [
        ('pc', '电脑端'),
        ('mobile', '移动端'),
    ]
    
    menu_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='菜单ID')
    parent_id = models.UUIDField(null=True, blank=True, verbose_name='父菜单ID')
    menu_name = models.CharField(max_length=50, verbose_name='菜单名称')
    path = models.CharField(max_length=200, verbose_name='路由路径')
    component = models.CharField(max_length=200, blank=True, null=True, verbose_name='前端组件路径')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='图标')
    sort = models.IntegerField(default=0, verbose_name='排序号')
    terminal = models.CharField(max_length=10, choices=TERMINAL_CHOICES, default='pc', verbose_name='终端类型')
    perm = models.ForeignKey(Permission, null=True, blank=True, on_delete=models.SET_NULL, 
                           related_name='menus', verbose_name='关联权限')
    is_show = models.BooleanField(default=True, verbose_name='是否显示')
    is_external = models.BooleanField(default=False, verbose_name='是否外部链接')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'tx_menus'
        verbose_name = '菜单'
        verbose_name_plural = '菜单'
        ordering = ['sort', 'create_time']
    
    def __str__(self):
        return self.menu_name


class RolePermission(models.Model):
    """角色权限关联表"""
    
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='权限')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'tx_role_permissions'
        verbose_name = '角色权限'
        verbose_name_plural = '角色权限'
        unique_together = ['role', 'permission']


class RoleMenu(models.Model):
    """角色菜单关联表"""
    
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name='菜单')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'tx_role_menus'
        verbose_name = '角色菜单'
        verbose_name_plural = '角色菜单'
        unique_together = ['role', 'menu']


class UserRole(models.Model):
    """用户角色关联表"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'tx_user_roles'
        verbose_name = '用户角色'
        verbose_name_plural = '用户角色'
        unique_together = ['user', 'role']


class OperationLog(models.Model):
    """操作日志模型"""
    
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='日志ID')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                           related_name='operation_logs', verbose_name='操作人')
    operation = models.CharField(max_length=100, verbose_name='操作内容')
    module = models.CharField(max_length=50, verbose_name='操作模块')
    ip_address = models.GenericIPAddressField(verbose_name='操作IP')
    user_agent = models.TextField(blank=True, null=True, verbose_name='用户代理')
    operation_time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    operation_result = models.BooleanField(verbose_name='操作结果')
    error_msg = models.TextField(null=True, blank=True, verbose_name='错误信息')
    
    class Meta:
        db_table = 'tx_operation_logs'
        verbose_name = '操作日志'
        verbose_name_plural = '操作日志'
        ordering = ['-operation_time']
    
    def __str__(self):
        return f"{self.user}-{self.operation}"


class SystemConfig(models.Model):
    """系统配置模型"""
    
    CONFIG_TYPE_CHOICES = [
        ('system', '系统配置'),
        ('security', '安全配置'),
        ('ui', '界面配置'),
        ('business', '业务配置'),
    ]
    
    config_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='配置ID')
    config_key = models.CharField(max_length=100, unique=True, verbose_name='配置键')
    config_value = models.TextField(verbose_name='配置值')
    config_type = models.CharField(max_length=20, choices=CONFIG_TYPE_CHOICES, 
                                 default='system', verbose_name='配置类型')
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='描述')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'tx_org_system_configs'
        verbose_name = '系统配置'
        verbose_name_plural = '系统配置'
        ordering = ['config_type', 'config_key']
    
    def __str__(self):
        return f"{self.config_key}: {self.config_value[:50]}"
