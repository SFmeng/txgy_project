"""
用户认证模型
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    """用户基础模型"""
    
    USER_TYPE_CHOICES = [
        ('enterprise', '企业用户'),
        ('individual', '个人用户'),
    ]
    
    STATUS_CHOICES = [
        ('active', '正常'),
        ('inactive', '未激活'),
        ('pending_review', '待审核'),
        ('banned', '已封禁'),
    ]
    
    user_id = models.CharField(max_length=32, unique=True, editable=False, verbose_name='用户ID')
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True, verbose_name='手机号码')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, verbose_name='用户类型')
    real_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='真实姓名')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='用户状态')
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='最后登录IP')
    
    class Meta:
        db_table = 'tx_users'
        verbose_name = '用户'
        verbose_name_plural = '用户'
    
    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self.generate_user_id()
        super().save(*args, **kwargs)
    
    def generate_user_id(self):
        """生成用户ID"""
        timestamp = datetime.now().strftime('%Y%m')
        # 获取当月最大序号
        last_user = User.objects.filter(
            user_id__startswith=f'USR-{timestamp}'
        ).order_by('-user_id').first()
        
        if last_user:
            last_seq = int(last_user.user_id.split('-')[-1])
            new_seq = last_seq + 1
        else:
            new_seq = 1
            
        return f'USR-{timestamp}-{new_seq:03d}'


class Enterprise(models.Model):
    """企业信息模型"""
    
    COMPANY_TYPE_CHOICES = [
        ('manufacturer', '生产制造企业'),
        ('constructor', '施工安装企业'),
        ('owner', '工程甲方企业'),
        ('supplier', '供应商企业'),
    ]
    
    CERTIFICATION_STATUS_CHOICES = [
        ('verified', '已认证'),
        ('pending', '待认证'),
        ('rejected', '认证失败'),
    ]
    
    RATING_CHOICES = [
        ('1star', '一星'),
        ('2star', '二星'),
        ('3star', '三星'),
        ('4star', '四星'),
        ('5star', '五星'),
    ]
    
    enterprise_id = models.CharField(max_length=32, primary_key=True, editable=False, verbose_name='企业ID')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='enterprise', verbose_name='关联用户')
    company_name = models.CharField(max_length=100, verbose_name='企业名称')
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES, verbose_name='企业类型')
    business_license = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='营业执照号')
    contact_person = models.CharField(max_length=50, null=True, blank=True, verbose_name='联系人')
    contact_phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='联系电话')
    contact_email = models.EmailField(null=True, blank=True, verbose_name='联系邮箱')
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='企业地址')
    province = models.CharField(max_length=20, null=True, blank=True, verbose_name='省份')
    city = models.CharField(max_length=20, null=True, blank=True, verbose_name='城市')
    district = models.CharField(max_length=20, null=True, blank=True, verbose_name='区县')
    business_scope = models.TextField(null=True, blank=True, verbose_name='经营范围')
    registered_capital = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='注册资本')
    established_year = models.PositiveIntegerField(null=True, blank=True, verbose_name='成立年份')
    annual_output = models.CharField(max_length=100, null=True, blank=True, verbose_name='年产量')
    employee_count = models.PositiveIntegerField(null=True, blank=True, verbose_name='员工数量')
    certification_status = models.CharField(max_length=20, choices=CERTIFICATION_STATUS_CHOICES, default='pending', verbose_name='认证状态')
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, null=True, blank=True, verbose_name='企业评级')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'tx_enterprises'
        verbose_name = '企业信息'
        verbose_name_plural = '企业信息'
    
    def save(self, *args, **kwargs):
        if not self.enterprise_id:
            self.enterprise_id = self.generate_enterprise_id()
        super().save(*args, **kwargs)
    
    def generate_enterprise_id(self):
        """生成企业ID"""
        timestamp = datetime.now().strftime('%Y%m')
        last_enterprise = Enterprise.objects.filter(
            enterprise_id__startswith=f'ENT-{timestamp}'
        ).order_by('-enterprise_id').first()
        
        if last_enterprise:
            last_seq = int(last_enterprise.enterprise_id.split('-')[-1])
            new_seq = last_seq + 1
        else:
            new_seq = 1
            
        return f'ENT-{timestamp}-{new_seq:03d}'
    
    def __str__(self):
        return self.company_name


class UserPermission(models.Model):
    """用户权限表"""
    
    permission_id = models.CharField(max_length=32, primary_key=True, editable=False, verbose_name='权限ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_permissions', verbose_name='用户')
    permission_code = models.CharField(max_length=50, verbose_name='权限代码')
    permission_name = models.CharField(max_length=100, verbose_name='权限名称')
    module_name = models.CharField(max_length=50, verbose_name='所属模块')
    granted_at = models.DateTimeField(auto_now_add=True, verbose_name='授权时间')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='过期时间')
    granted_by = models.CharField(max_length=32, null=True, blank=True, verbose_name='授权人ID')
    
    class Meta:
        db_table = 'tx_user_permissions'
        verbose_name = '用户权限'
        verbose_name_plural = '用户权限'
        unique_together = ['user', 'permission_code']
    
    def save(self, *args, **kwargs):
        if not self.permission_id:
            import uuid
            self.permission_id = str(uuid.uuid4()).replace('-', '')
        super().save(*args, **kwargs)
