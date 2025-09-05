"""
主URL配置
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API文档配置
schema_view = get_schema_view(
    openapi.Info(
        title="防腐保温智慧平台 API",
        default_version='v1',
        description="防腐保温行业信息交互平台API文档",
        terms_of_service="https://www.txgy-platform.com/terms/",
        contact=openapi.Contact(email="dev@txgy-platform.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # 管理后台
    path('admin/', admin.site.urls),
    
    # API文档
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API路由
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/organization/', include('apps.organization.urls')),
    path('api/v1/info/', include('apps.info_publish.urls')),
    path('api/v1/search/', include('apps.search_match.urls')),
    path('api/v1/communication/', include('apps.communication.urls')),
    path('api/v1/resources/', include('apps.resources.urls')),
    path('api/v1/business/', include('apps.business.urls')),
    path('api/v1/tech-service/', include('apps.tech_service.urls')),
    path('api/v1/bidding/', include('apps.bidding.urls')),
    path('api/v1/data/', include('apps.data_center.urls')),
    path('api/v1/common/', include('apps.common.urls')),
]

# 静态文件和媒体文件URL配置
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # 开发环境调试工具
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

# 自定义管理后台标题
admin.site.site_header = '防腐保温智慧平台管理后台'
admin.site.site_title = '防腐保温智慧平台'
admin.site.index_title = '欢迎使用防腐保温智慧平台管理后台'
