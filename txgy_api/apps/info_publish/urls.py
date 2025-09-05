"""
信息发布模块URL配置
"""
from django.urls import path
from . import views

app_name = 'info_publish'

urlpatterns = [
    # 供应信息
    path('supply/', views.supply_list, name='supply_list'),
    path('supply/create/', views.supply_create, name='supply_create'),
    
    # 采购需求
    path('demand/', views.demand_list, name='demand_list'),
    path('demand/create/', views.demand_create, name='demand_create'),
    
    # 招聘信息
    path('recruitment/', views.recruitment_list, name='recruitment_list'),
    path('recruitment/create/', views.recruitment_create, name='recruitment_create'),
]
