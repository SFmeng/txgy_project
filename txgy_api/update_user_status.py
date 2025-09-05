#!/usr/bin/env python
"""
更新用户状态脚本
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# 更新所有用户状态为active
users_updated = User.objects.filter(status='pending_review').update(status='active')
print(f"✅ 已更新 {users_updated} 个用户状态为激活")

# 显示所有用户状态
users = User.objects.all()
print("\n📋 当前用户状态:")
for user in users:
    print(f"- {user.username}: {user.status} ({'激活' if user.is_active else '未激活'})")

print("\n✅ 用户状态更新完成")
