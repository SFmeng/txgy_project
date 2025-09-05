"""
公共模块管理后台
"""
from django.contrib import admin
from .models import Region, Category, FileUpload, SystemConfig


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    """地区管理"""
    list_display = ['code', 'name', 'level', 'parent', 'sort_order', 'is_active']
    list_filter = ['level', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['sort_order', 'code']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """分类管理"""
    list_display = ['name', 'code', 'category_type', 'parent', 'level', 'sort_order', 'is_active']
    list_filter = ['category_type', 'level', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['sort_order', 'code']


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    """文件上传管理"""
    list_display = ['original_name', 'file_type', 'file_size', 'uploaded_by', 'created_at']
    list_filter = ['file_type', 'created_at']
    search_fields = ['original_name', 'uploaded_by']
    readonly_fields = ['file_id', 'created_at']


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    """系统配置管理"""
    list_display = ['key', 'config_type', 'description', 'is_active', 'updated_at']
    list_filter = ['config_type', 'is_active']
    search_fields = ['key', 'description']
