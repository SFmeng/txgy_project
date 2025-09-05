#!/usr/bin/env python3
"""
测试序列化器
"""
import os
import sys
import django

# 设置Django环境
os.chdir('txgy_api')
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'txgy_api.settings')
django.setup()

from apps.authentication.models import User, Enterprise
from apps.authentication.serializers import UserManagementSerializer

def test_serializer():
    print('🧪 测试序列化器...')
    
    # 检查企业用户
    enterprise_user = User.objects.filter(user_type='enterprise').first()
    if enterprise_user:
        print(f'企业用户: {enterprise_user.username}')
        print(f'hasattr enterprise: {hasattr(enterprise_user, "enterprise")}')
        
        try:
            enterprise = enterprise_user.enterprise
            print(f'企业记录存在: {enterprise.company_name}')
            print(f'认证状态: {enterprise.certification_status}')
        except Exception as e:
            print(f'获取企业记录失败: {e}')
        
        # 测试序列化器
        serializer = UserManagementSerializer(enterprise_user)
        data = serializer.data
        print(f'序列化后的enterprise_info: {data.get("enterprise_info")}')
        print(f'序列化后的roles: {data.get("roles")}')
    else:
        print('没有找到企业用户')

if __name__ == '__main__':
    test_serializer()
