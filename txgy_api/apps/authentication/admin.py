"""
用户认证管理后台配置
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Enterprise, UserPermission


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    
    list_display = [
        'user_id', 'username', 'real_name', 'phone', 'user_type', 
        'status', 'is_active', 'date_joined', 'last_login'
    ]
    list_filter = ['user_type', 'status', 'is_active', 'date_joined']
    search_fields = ['username', 'real_name', 'phone', 'email', 'user_id']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {
            'fields': ('real_name', 'email', 'phone', 'avatar')
        }),
        ('用户类型', {
            'fields': ('user_type', 'status')
        }),
        ('权限', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('重要日期', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type'),
        }),
    )
    
    readonly_fields = ['user_id', 'date_joined', 'last_login']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('enterprise')


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    """企业信息管理"""
    
    list_display = [
        'enterprise_id', 'company_name', 'company_type', 'contact_person',
        'certification_status', 'rating', 'created_at'
    ]
    list_filter = ['company_type', 'certification_status', 'rating', 'province', 'city']
    search_fields = ['company_name', 'business_license', 'contact_person', 'enterprise_id']
    ordering = ['-created_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('company_name', 'company_type', 'business_license')
        }),
        ('联系信息', {
            'fields': ('contact_person', 'contact_phone', 'contact_email')
        }),
        ('地址信息', {
            'fields': ('address', 'province', 'city', 'district')
        }),
        ('企业详情', {
            'fields': ('business_scope', 'registered_capital', 'established_year', 
                      'annual_output', 'employee_count'),
            'classes': ('collapse',)
        }),
        ('认证信息', {
            'fields': ('certification_status', 'rating')
        }),
    )
    
    readonly_fields = ['enterprise_id', 'created_at', 'updated_at']
    
    actions = ['approve_certification', 'reject_certification']
    
    def approve_certification(self, request, queryset):
        """批准企业认证"""
        updated = queryset.update(certification_status='verified')
        self.message_user(request, f'已批准 {updated} 个企业的认证申请')
    approve_certification.short_description = '批准选中的企业认证'
    
    def reject_certification(self, request, queryset):
        """拒绝企业认证"""
        updated = queryset.update(certification_status='rejected')
        self.message_user(request, f'已拒绝 {updated} 个企业的认证申请')
    reject_certification.short_description = '拒绝选中的企业认证'


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    """用户权限管理"""
    
    list_display = [
        'permission_id', 'user', 'permission_name', 'module_name',
        'granted_at', 'expires_at', 'is_expired'
    ]
    list_filter = ['module_name', 'granted_at', 'expires_at']
    search_fields = ['user__username', 'permission_code', 'permission_name']
    ordering = ['-granted_at']
    
    fieldsets = (
        ('权限信息', {
            'fields': ('user', 'permission_code', 'permission_name', 'module_name')
        }),
        ('授权信息', {
            'fields': ('granted_at', 'expires_at', 'granted_by')
        }),
    )
    
    readonly_fields = ['permission_id', 'granted_at']
    
    def is_expired(self, obj):
        """检查权限是否过期"""
        if obj.expires_at:
            from django.utils import timezone
            if obj.expires_at < timezone.now():
                return format_html('<span style="color: red;">已过期</span>')
            else:
                return format_html('<span style="color: green;">有效</span>')
        return format_html('<span style="color: blue;">永久</span>')
    is_expired.short_description = '状态'


# 自定义管理后台标题
admin.site.site_header = '防腐保温智慧平台管理后台'
admin.site.site_title = '防腐保温智慧平台'
admin.site.index_title = '欢迎使用防腐保温智慧平台管理后台'
