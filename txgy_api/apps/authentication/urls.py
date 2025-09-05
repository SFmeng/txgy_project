"""
用户认证URL配置
"""
from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # 用户认证
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # 用户信息
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    
    # 密码管理
    path('password/change/', views.change_password, name='change_password'),
    path('password/reset/', views.reset_password, name='reset_password'),
    
    # 短信验证码
    path('sms/send/', views.send_sms_code, name='send_sms_code'),

    # 用户管理
    path('users/', views.user_management, name='user_management'),
    path('users/<str:user_id>/', views.user_detail, name='user_detail'),

    # 企业认证
    path('enterprise/verify/', views.enterprise_verify, name='enterprise_verify'),

    # 统计数据
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),

    # 用户权限
    path('permissions/', views.user_permissions, name='user_permissions'),
]
