#!/usr/bin/env python3
"""
修复企业用户数据 - 为企业用户创建Enterprise记录
"""
import os
import sys
import django

# 设置Django环境
sys.path.append('txgy_api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'txgy_api.settings')
django.setup()

from apps.authentication.models import User, Enterprise
from apps.organization.models import Role, UserRole

def fix_enterprise_data():
    print('🔧 修复企业用户数据...')
    print('=' * 50)
    
    # 1. 为企业用户创建Enterprise记录
    enterprise_users = User.objects.filter(user_type='enterprise')
    print(f'找到 {enterprise_users.count()} 个企业用户')
    
    created_count = 0
    for user in enterprise_users:
        enterprise, created = Enterprise.objects.get_or_create(
            user=user,
            defaults={
                'company_name': user.real_name or f'{user.username}公司',
                'company_type': 'manufacturer',
                'certification_status': 'pending',
                'contact_person': user.real_name or user.username,
                'contact_phone': user.phone or '',
                'contact_email': user.email or '',
                'address': '待完善',
                'business_scope': '待完善',
            }
        )
        
        if created:
            created_count += 1
            print(f'✅ 为用户 {user.username} 创建企业记录')
        else:
            print(f'📋 用户 {user.username} 已有企业记录')
    
    print(f'共创建了 {created_count} 个企业记录')
    
    # 2. 检查角色分配
    print('\n🎭 检查角色分配...')
    roles = Role.objects.all()
    print(f'系统中有 {roles.count()} 个角色')
    
    # 为admin用户分配超级管理员角色
    admin_user = User.objects.filter(username='admin').first()
    if admin_user:
        admin_role = Role.objects.filter(role_name__icontains='管理员').first()
        if admin_role:
            user_role, created = UserRole.objects.get_or_create(
                user=admin_user,
                role=admin_role
            )
            if created:
                print(f'✅ 为admin用户分配角色: {admin_role.role_name}')
            else:
                print(f'📋 admin用户已有角色: {admin_role.role_name}')
    
    # 3. 验证数据
    print('\n📊 验证修复结果...')
    
    # 检查企业用户的enterprise_info
    from apps.authentication.serializers import UserManagementSerializer
    
    enterprise_users_with_info = 0
    for user in enterprise_users:
        serializer = UserManagementSerializer(user)
        data = serializer.data
        if data.get('enterprise_info'):
            enterprise_users_with_info += 1
    
    print(f'有企业信息的企业用户: {enterprise_users_with_info}/{enterprise_users.count()}')
    
    # 检查用户角色
    users_with_roles = UserRole.objects.count()
    print(f'有角色分配的用户: {users_with_roles}')
    
    print('\n✅ 数据修复完成！')

if __name__ == '__main__':
    fix_enterprise_data()
