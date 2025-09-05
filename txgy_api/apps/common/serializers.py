"""
公共模块序列化器
"""
from rest_framework import serializers
from .models import Region, Category, FileUpload, SystemConfig


class RegionSerializer(serializers.ModelSerializer):
    """地区序列化器"""
    
    class Meta:
        model = Region
        fields = ['code', 'name', 'level', 'parent', 'sort_order']


class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    
    class Meta:
        model = Category
        fields = ['category_id', 'name', 'code', 'category_type', 'parent', 'level', 'description', 'icon']


class FileUploadSerializer(serializers.ModelSerializer):
    """文件上传序列化器"""
    
    class Meta:
        model = FileUpload
        fields = ['file_id', 'original_name', 'file_path', 'file_size', 'file_type', 'created_at']
        read_only_fields = ['file_id', 'created_at']


class SystemConfigSerializer(serializers.ModelSerializer):
    """系统配置序列化器"""
    
    class Meta:
        model = SystemConfig
        fields = ['key', 'value', 'config_type', 'description']
