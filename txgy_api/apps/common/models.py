"""
公共模型
"""
from django.db import models


class BaseModel(models.Model):
    """基础模型类"""
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        abstract = True


class Region(models.Model):
    """地区模型"""
    
    LEVEL_CHOICES = [
        ('province', '省份'),
        ('city', '城市'),
        ('district', '区县'),
    ]
    
    code = models.CharField(max_length=20, unique=True, verbose_name='地区代码')
    name = models.CharField(max_length=50, verbose_name='地区名称')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name='级别')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='上级地区')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    
    class Meta:
        db_table = 'tx_regions'
        verbose_name = '地区'
        verbose_name_plural = '地区'
        ordering = ['sort_order', 'code']
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """分类模型"""
    
    CATEGORY_TYPE_CHOICES = [
        ('product', '产品分类'),
        ('service', '服务分类'),
        ('industry', '行业分类'),
    ]
    
    category_id = models.CharField(max_length=32, primary_key=True, editable=False, verbose_name='分类ID')
    name = models.CharField(max_length=100, verbose_name='分类名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='分类代码')
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES, verbose_name='分类类型')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父分类')
    level = models.PositiveIntegerField(default=1, verbose_name='层级')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='排序')
    description = models.TextField(null=True, blank=True, verbose_name='描述')
    icon = models.CharField(max_length=100, null=True, blank=True, verbose_name='图标')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'tx_categories'
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['sort_order', 'code']
    
    def save(self, *args, **kwargs):
        if not self.category_id:
            import uuid
            self.category_id = str(uuid.uuid4()).replace('-', '')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class FileUpload(models.Model):
    """文件上传记录"""
    
    FILE_TYPE_CHOICES = [
        ('image', '图片'),
        ('document', '文档'),
        ('video', '视频'),
        ('other', '其他'),
    ]
    
    file_id = models.CharField(max_length=32, primary_key=True, editable=False, verbose_name='文件ID')
    original_name = models.CharField(max_length=255, verbose_name='原始文件名')
    file_name = models.CharField(max_length=255, verbose_name='存储文件名')
    file_path = models.CharField(max_length=500, verbose_name='文件路径')
    file_size = models.PositiveIntegerField(verbose_name='文件大小(字节)')
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, verbose_name='文件类型')
    mime_type = models.CharField(max_length=100, verbose_name='MIME类型')
    uploaded_by = models.CharField(max_length=32, verbose_name='上传用户ID')
    upload_ip = models.GenericIPAddressField(verbose_name='上传IP')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    
    class Meta:
        db_table = 'tx_file_uploads'
        verbose_name = '文件上传'
        verbose_name_plural = '文件上传'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.file_id:
            import uuid
            self.file_id = str(uuid.uuid4()).replace('-', '')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.original_name


class SystemConfig(models.Model):
    """系统配置"""
    
    CONFIG_TYPE_CHOICES = [
        ('system', '系统配置'),
        ('business', '业务配置'),
        ('ui', '界面配置'),
    ]
    
    key = models.CharField(max_length=100, unique=True, verbose_name='配置键')
    value = models.TextField(verbose_name='配置值')
    config_type = models.CharField(max_length=20, choices=CONFIG_TYPE_CHOICES, default='system', verbose_name='配置类型')
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='描述')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'tx_system_configs'
        verbose_name = '系统配置'
        verbose_name_plural = '系统配置'
        ordering = ['config_type', 'key']
    
    def __str__(self):
        return f"{self.key}: {self.value[:50]}"
