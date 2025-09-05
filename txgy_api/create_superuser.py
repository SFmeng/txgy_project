#!/usr/bin/env python
"""
创建超级用户脚本
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# 检查是否已存在超级用户
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@txgy.com',
        password='admin123456',
        user_type='enterprise',
        real_name='系统管理员'
    )
    print("✅ 超级用户创建成功")
    print("用户名: admin")
    print("密码: admin123456")
    print("邮箱: admin@txgy.com")
else:
    print("ℹ️ 超级用户已存在")
