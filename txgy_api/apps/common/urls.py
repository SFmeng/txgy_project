"""
公共模块URL配置
"""
from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    # 地区相关
    path('regions/', views.region_list, name='region_list'),
    path('regions/<str:parent_code>/children/', views.region_children, name='region_children'),
    
    # 分类相关
    path('categories/', views.category_list, name='category_list'),
    path('categories/<str:category_type>/', views.category_by_type, name='category_by_type'),
    
    # 文件上传
    path('upload/', views.file_upload, name='file_upload'),
    
    # 系统配置
    path('configs/', views.system_configs, name='system_configs'),
]
