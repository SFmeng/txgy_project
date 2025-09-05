"""
用户认证序列化器
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.cache import cache
from .models import User, Enterprise


class UserRegistrationSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""

    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    verification_code = serializers.CharField(write_only=True, max_length=6, required=False)
    enterprise_info = serializers.DictField(required=False, write_only=True)
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'phone', 'user_type', 'real_name',
            'password', 'password_confirm', 'verification_code', 'enterprise_info'
        ]
    
    def validate(self, attrs):
        # 验证密码确认
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("两次输入的密码不一致")
        
        # 验证手机号格式
        phone = attrs.get('phone')
        if phone and not phone.isdigit() or len(phone) != 11:
            raise serializers.ValidationError("手机号格式不正确")
        
        # 验证短信验证码（开发环境可选）
        verification_code = attrs.get('verification_code')
        if phone and verification_code:  # 只有提供了验证码才进行验证
            cached_code = cache.get(f'sms_code_{phone}')
            if cached_code and cached_code != verification_code:
                raise serializers.ValidationError("验证码错误或已过期")
        
        return attrs
    
    def create(self, validated_data):
        # 移除不需要保存到User模型的字段
        validated_data.pop('password_confirm')
        validated_data.pop('verification_code', None)  # 使用默认值None，避免KeyError
        enterprise_info = validated_data.pop('enterprise_info', {})
        
        # 创建用户
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        
        # 如果是企业用户，创建企业信息
        if user.user_type == 'enterprise' and enterprise_info:
            Enterprise.objects.create(user=user, **enterprise_info)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    
    username = serializers.CharField()
    password = serializers.CharField()
    login_type = serializers.CharField(default='password')
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            # 尝试用户名登录
            user = authenticate(username=username, password=password)
            
            # 如果用户名登录失败，尝试手机号登录
            if not user:
                try:
                    user_obj = User.objects.get(phone=username)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if not user:
                raise serializers.ValidationError("用户名或密码错误")
            
            if not user.is_active:
                raise serializers.ValidationError("用户账号已被禁用")
            
            if user.status == 'banned':
                raise serializers.ValidationError("账号已被封禁")
            elif user.status == 'pending_review':
                raise serializers.ValidationError("账号待审核，请耐心等待")
            
            attrs['user'] = user
        else:
            raise serializers.ValidationError("用户名和密码不能为空")
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""

    enterprise_info = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email', 'phone', 'user_type',
            'real_name', 'avatar', 'status', 'date_joined',
            'enterprise_info', 'roles', 'permissions'
        ]
        read_only_fields = ['user_id', 'username', 'user_type', 'status', 'date_joined']

    def get_enterprise_info(self, obj):
        if obj.user_type == 'enterprise' and hasattr(obj, 'enterprise'):
            return EnterpriseSerializer(obj.enterprise).data
        return None

    def get_roles(self, obj):
        """获取用户角色"""
        from apps.organization.models import UserRole
        user_roles = UserRole.objects.filter(user=obj).select_related('role')
        return [
            {
                'role_id': ur.role.role_id,
                'role_name': ur.role.role_name,
                'description': ur.role.description
            }
            for ur in user_roles
        ]

    def get_permissions(self, obj):
        """获取用户权限"""
        from apps.organization.models import UserRole, RolePermission

        # 获取用户所有角色的权限
        user_roles = UserRole.objects.filter(user=obj).values_list('role_id', flat=True)
        role_permissions = RolePermission.objects.filter(
            role_id__in=user_roles
        ).select_related('permission')

        permissions = []
        seen_permissions = set()

        for rp in role_permissions:
            if rp.permission.perm_id not in seen_permissions:
                permissions.append({
                    'perm_id': rp.permission.perm_id,
                    'perm_name': rp.permission.perm_name,
                    'perm_code': rp.permission.perm_code,
                    'module': rp.permission.module,
                    'action': rp.permission.action
                })
                seen_permissions.add(rp.permission.perm_id)

        return permissions


class UserManagementSerializer(serializers.ModelSerializer):
    """用户管理序列化器"""

    enterprise_info = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email', 'phone', 'user_type',
            'real_name', 'avatar', 'status', 'date_joined', 'last_login',
            'enterprise_info', 'roles'
        ]
        read_only_fields = ['user_id', 'date_joined', 'last_login']

    def get_enterprise_info(self, obj):
        if obj.user_type == 'enterprise':
            try:
                return EnterpriseSerializer(obj.enterprise).data
            except Enterprise.DoesNotExist:
                return None
        return None

    def get_roles(self, obj):
        """获取用户角色"""
        from apps.organization.models import UserRole
        user_roles = UserRole.objects.filter(user=obj).select_related('role')
        return [
            {
                'role_id': ur.role.role_id,
                'role_name': ur.role.role_name,
                'description': ur.role.description
            }
            for ur in user_roles
        ]


class EnterpriseSerializer(serializers.ModelSerializer):
    """企业信息序列化器"""
    
    class Meta:
        model = Enterprise
        fields = [
            'enterprise_id', 'company_name', 'company_type', 'business_license',
            'contact_person', 'contact_phone', 'contact_email', 'address',
            'province', 'city', 'district', 'business_scope', 'registered_capital',
            'established_year', 'annual_output', 'employee_count',
            'certification_status', 'rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['enterprise_id', 'certification_status', 'rating', 'created_at', 'updated_at']


class PasswordChangeSerializer(serializers.Serializer):
    """修改密码序列化器"""
    
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=6)
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("两次输入的新密码不一致")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("原密码错误")
        return value


class PasswordResetSerializer(serializers.Serializer):
    """重置密码序列化器"""
    
    phone = serializers.CharField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=6)
    
    def validate(self, attrs):
        phone = attrs.get('phone')
        code = attrs.get('code')
        
        # 验证手机号是否存在
        try:
            user = User.objects.get(phone=phone)
            attrs['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError("手机号未注册")
        
        # 验证短信验证码
        cached_code = cache.get(f'sms_code_{phone}')
        if not cached_code or cached_code != code:
            raise serializers.ValidationError("验证码错误或已过期")
        
        return attrs


class SmsCodeSerializer(serializers.Serializer):
    """短信验证码序列化器"""
    
    phone = serializers.CharField()
    type = serializers.ChoiceField(choices=['register', 'reset_password', 'change_phone'])
    
    def validate_phone(self, value):
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("手机号格式不正确")
        return value
